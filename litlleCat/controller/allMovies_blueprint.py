# 这里是蓝图：返回全部电源的简单信息
# 前端可以对这些分页展示
# pre-fix： /
from flask import Blueprint, request, g
from sqlalchemy import func, or_

from common.model.movies import Movie
from common.model.comment import Comment
from common.model.history import History
from common.model.users import User
from common.lib.DataHelper import getCurrentTime
from common.model.classificationName import Classificationname
from application import db_mysql
from common.lib.helper import ops_renderJSON, ops_renderErrJSON
import math, requests
from common.lib.helper import JsonHelper
from interceptors.Auth import check_login           # ？ 必须引用它，否则 g.current_user 找不到


# 创建一个蓝图
allMovies_blueprint_page = Blueprint("allMovies_blueprint_page", __name__)
aPage_size = 30             # 一个页面的电影数量


'''
# 函数：    allMovies_allClass
# address： /allClass
# 功能：    为全部分类提供电源列列表，根据参数以筛选；
            搜索功能： 电影名、演员名、导演名 ==》 search
            全部筛选条件可以同时存在； 比如：class=爱情； actor=xx;...
# 参数：    无强制参数
            可选参数：
            page_request: 请求哪一页， 默认第一页; 只换页的时候 其他条件要保持和上一次一样
                           
            orderBy_condition: 排序条件; 格式：字段名#升降序; (asc/desc)
                  其中"#" 是分割符，分割字段名和升降序条件
                  排序字段：
                        可以是：pub_date；view_count；comment_count; love_count douban_score;
                        默认：douban_score
                  升降序： 默认降序
                  ex:  pub_date#desc ;  pub_date#asc
#           class：  类型，返回标签里有该关键词的电影
                     另有方法提供所有 类名
                     ex： http://127.0.0.1:5000/allClass?class=爱情
#           area：   地区，返回该地区的电影
                     另有方法提供所有 地区名 
#           year:    年份，返回该年分上映的电影                       
                     年份：近3--5年吧，空就是没有
#           search:  搜索字段， 将自动检索：电影名、电影又名、主演名、导演名
                     返回同样是电影列表（可能为空）
                     search=xxx名                                         
# 返回：   标准响应：code=200, msg="movie list and pageInfo", data={"movieList" : movieList，"pageInfo":pageInfo }
#          参数名错了/名对值错 ==》 参数无效：
#          错误：code = -1, msg = "搜索词不合法", data={}         
mo
vieList = [ {}, {}, ..... ]
#          key_name = ["movie_id", "name", "cover_pic","comment_count","douban_score", "classification"]
#           pageInfo:{
#               "page_cur":     请求的页面号，默认是第一页
#               "aPage_size":   一页的大小,
#               "total_count":  电影总数
#               "total_pages":  总页数
#               "is_prev":      是否有前一页,1/0
#               "is_next":      是否有后一页,1/0
#               } 
'''
@allMovies_blueprint_page.route("/allClass", methods=["GET", "POST"])
def allMovies_allClass():
    # 请求信息
    reqInfo = request.values
    page_request = reqInfo["page_request"] if "page_request" in reqInfo else 1  # 请求的页面号
    page_request = int(page_request)
    classification = reqInfo["class"] if "class" in reqInfo else None           # 类型要求
    area = reqInfo["area"] if "area" in reqInfo else None                       # 地区
    year = reqInfo["year"] if "year" in reqInfo else None                       # year
    search = reqInfo["search"] if "search" in reqInfo else None                 # search

    # 排序条件: pub_date；view_count；comment_count; love_count; douban_score; 默认 douban_score
    orderBy_condition_req = reqInfo["orderBy_condition"] if "orderBy_condition" in reqInfo else None
    orderBy_condition = get_orderBy_condition(orderBy_condition_req)

    # 根据请求，向数据库请求Movies
    # "movie_id", "name", "cover_pic","comment_count","douban_score", "class"
    movies_query_list = db_mysql.session.query(Movie.movie_id, Movie.name, Movie.cover_pic, Movie.comment_count,
                                               Movie.douban_score, Movie.classification)
    colums_name = ["movie_id", "name", "cover_pic", "comment_count", "douban_score", "classification"]

    # 按照class（classification in db） 筛选
    if classification is not None:
        movies_query_list = movies_query_list.\
            filter(Movie.classification.like("%#%".replace("#", classification )))
    # 按 地区 筛选
    if area is not None:
        movies_query_list = movies_query_list.\
            filter(Movie.area.like("%#%".replace("#", area)))
    # 按 年份 筛选
    if year is not None:
        movies_query_list = movies_query_list. \
            filter(Movie.year.like("%#%".replace("#", year)))


    # 按 搜索词 筛选
    # 关键词优化： 优先搜索 电影名字、主演、导演
    # ####### 先去除 非意义字符
    if search is not None:
        search = validWord_serach(search)
        if len(search) < 1:
            return ops_renderErrJSON(msg="搜索词不合法")
        movies_query_list_tmp = movies_query_list
        # 按电影名字
        movies_query_list = movies_query_list.\
            filter( Movie.name.like("%#%".replace("#", search))).all()

        # 如果没有结果,按 主演名字
        if len(movies_query_list) < 1:
            movies_query_list = movies_query_list_tmp
            movies_query_list = movies_query_list. \
                filter(Movie.actors.like("%#%".replace("#", search))).all()
        # 如果没有结果,按导演名字
        if len(movies_query_list) < 1:
            movies_query_list = movies_query_list_tmp
            movies_query_list = movies_query_list. \
                filter(Movie.director.like("%#%".replace("#", search))).all()

        # 直接返回 不和其他情况一起？  多出口不好，还挺复杂1!!
        movies_query_list_return = JsonHelper.json_sqlAlchemy_list(movies_query_list, colums_name)
        return ops_renderJSON(data={"movieList" : movies_query_list_return})


    # 页面信息 ！！ 页面信息必须是在所有的筛之后！
    total_size = movies_query_list.count()  # 电影总数量
    total_pages = math.ceil(total_size / aPage_size)  # 总页数， 向上取整
    is_prev = 0 if page_request <= 1 else 1  # 是否有前一页
    is_next = 0 if page_request >= total_pages else 1  # 是否有后一页
    # 发送的页面信息
    page = {
        "page_cur": page_request,
        "aPage_size": aPage_size,
        "total_count": total_size,
        "total_pages": total_pages,
        "is_prev": is_prev,
        "is_next": is_next
    }
    # 排序 和 页面范围
    # 页面电影的范围： 0 - 30,30 - 60 ,60 - 90
    offset = (page_request - 1) * aPage_size
    limit = page_request * aPage_size
    # 注意 需要第二排序条件， 否则顺序会变动
    movie_list = movies_query_list.order_by(orderBy_condition, Movie.movie_id.asc())[offset:limit]

    # 把 movie_list ==》 dict ==》  json化
    movie_list_json = JsonHelper.json_sqlAlchemy_list(movie_list, colums_name)
    return_dict = {"pageInfo": page, "movieList": movie_list_json}

    return ops_renderJSON(data=return_dict)

# 搜索词 合法化
# 无法合法化 ==》 len = 0
def validWord_serach(strIn):
    invalid_set = {"%", "-", "+", "*", "&", "#", "$", "_"}
    strNew = ""
    for ch in strIn:
        if ch not in invalid_set:
            strNew += ch

    return strNew



'''
# 函数：   allMovies_staticInfo
# 功能：   通过参数获取 相应的信息（静态信息，如分类的所有类名）
# 地址：   /static/强制参数
# 参数：   强制参数 即/static/ 后不能为空
#               可以是： classNames：返回 [全部的类的名字];  
                         areaNames:  返回 [全部地区的名字]
# 示例:    /static/classNames ； 注意 复数+s
# 返回：   根据 static 后的内容 将返回相应的信息； 如所有分类类名
#          标准响应：code=200, msg="success", data={"强制参数":数据 }
#          错误 code=-1, msg="no such operation"
#
# 简单理解为：    访问 ip/static/classNames 则返回所有分类的类名
# 例：    { code=200, msg="success", data={"classNames": ["传记", "体育", "儿童", "剧情", "动作", "动画", "励志", "历史", "古装", "同性",
# #                "喜剧", "奇幻", "家庭", "恐怖", "悬疑", "惊悚", "战争", "校园", "歌舞", "武侠", 
# #                "灾难", "爱情", "犯罪", "短片", "科幻", "纪录", "脱口秀", "西部", "谍战", "运动",
# #                 "青春", "音乐", "黑色电影"]}
#           }
# 
'''
@allMovies_blueprint_page.route("/static/<info>", methods=["GET", "POST"])
def allMovies_staticInfo(info):
    info_req = info
    # 根据 info的信息来执行不同的操作
    return_dict = {}
    if info_req == "classNames":                     # 返回所有分类的类名
        class_query = db_mysql.session.query(Classificationname.name)
        # 写出 dict
        lst = []
        for content in class_query:         # [ ["传记"], ["武侠"],.....]
            lst.append(content[0])
        return_dict["classNames"] = lst
        return ops_renderJSON(msg=info, data=JsonHelper.json_dict(return_dict))

    if info_req == "areaNames":
        from common.model.areaName import AreaName
        area_query = db_mysql.session.query(AreaName.name)
        # 写出 dict
        lst = []
        for content in area_query:  # [ ["xxx"], ["xxx"],.....]
            lst.append(content[0])
        return_dict["areaNames"] = lst
        return ops_renderJSON(msg=info, data=JsonHelper.json_dict(return_dict))

    return ops_renderErrJSON(msg="no such operation")


# 参数：排序条件字符串
# 返回：排序主条件；默认douban_score.desc()
def get_orderBy_condition(orderBy_condition):
    # default ：
    orderBy_condition_first = Movie.douban_score                        # 默认主条件
    # else
    if orderBy_condition is not None:                                   # 有设置排序条件
        orderBy_condition.strip()                                       # 去首尾空格
        orderBy_condition_split = orderBy_condition.split("#", 1)       # 分离参数

        # 排序条件
        # 可以是：pub_date；view_count；comment_count; love_count douban_score;
        if orderBy_condition_split[0] == "view_count":
            orderBy_condition_first = Movie.view_count
        if orderBy_condition_split[0] == "pub_date":
            orderBy_condition_first = Movie.pub_date
        if orderBy_condition_split[0] == "comment_count":
            orderBy_condition_first = Movie.comment_count
        if orderBy_condition_split[0] == "love_count":
            orderBy_condition_first = Movie.love_count
        # 升降序
        if len(orderBy_condition_split) < 2 or orderBy_condition_split[1] == "desc"   :
            orderBy_condition_first = orderBy_condition_first.desc()
        else:
            orderBy_condition_first = orderBy_condition_first.asc()
    else:
        orderBy_condition_first = orderBy_condition_first.desc()

    return orderBy_condition_first



'''
# 函数：   allMovies_movieInfo
# 功能：   返回电影的详细信息
# 地址：   /movieInfo/强制参数<movie_id>, movie_id 电影的唯一标识,在电影列表里有该id
# 参数：   强制参数 即/movieInfo/ 后不能为空
#               可以是： 某一部电影的movie_id;
# 示例:    /movieInfo/44 ； 
# 返回：   根据 movie_id  将返回相应电影的详细信息
#          标准响应：code=200, msg="movie info ", data={信息项名:信息 }
#          错误 code=-1, msg="no such movie"
#          电影的详情信息项有：
#          movie_id,name, classification,actors,cover_pic,pics,description,imdb_url,vid_url
#          pub_date,source,view_count,douban_score,love_count,comment_count,director, 
#          other_name, area, info_url
#          增加返回项： stared 如果用户登录了： 该电影是否已经被收藏 0/1
                                如果没有登录: 返回没有收藏 0

# 例子：   /movieInfo/44 返回
#          { code=200, msg="movie_info", data={"movie_id":44, "name":"惊奇先生", .....}
#           }
'''
@allMovies_blueprint_page.route("/movieInfo/<movie_id>", methods=["GET", "POST"])
def allMovies_movieInfo(movie_id):
    # 电影是否存在
    movie_exit = db_mysql.session.query(Movie.movie_id).filter(Movie.movie_id == movie_id).first()
    if movie_exit is None:
        return ops_renderErrJSON(msg="no such movie")

    # 获取该电影的所有信息
    movie_query = db_mysql.session.query(Movie.movie_id, Movie.name, Movie.classification, Movie.actors, Movie.cover_pic,
                                         Movie.pics, Movie.description, Movie.imdb_url, Movie.vid_url,Movie.pub_date,
                                         Movie.source, Movie.view_count, Movie.douban_score, Movie.love_count,
                                         Movie.comment_count, Movie.director, Movie.other_name, Movie.area,
                                         Movie.info_url).filter(Movie.movie_id == movie_id).first()

    if movie_query is None:
        return ops_renderErrJSON(msg="no such movie")
    # 获取 colums_name
    colums_name = ["movie_id", "name", "classification", "actors", "cover_pic", "pics", "description", "imdb_url",
                   "vid_url", "pub_date", "source", "view_count", "douban_score", "love_count",
                   "comment_count", "director", "other_name", "area", "info_url"]

    # 合成字典形式
    movieInfo_dict = JsonHelper.list_to_dict(colums_name, movie_query)

    # 阅读量+1
    mq = Movie.query.filter(movie_id == movie_id).first()
    mq.view_count += 1
    db_mysql.session.add(mq)
    db_mysql.session.commit()

    # 对 数据库里 冒失 list的str进行转成list
    # str = ["http://gif-china.cc/uploads/allimg/202003/1d2dd4f9979b2755.jpg?h=250", "sdfsdasf"]
    movieInfo_dict["pics"] = JsonHelper.str_to_list( movieInfo_dict["pics"])

    # 添加： 如果已登录，是否已收藏？
    movieInfo_dict["stared"] = 0
    # 从cookie读取用户信息
    usr_info = g.current_user
    if usr_info is not None:                # 已登录
        usr_id = usr_info.usr_id
        # 是否已经收藏
        isExit = History.query.filter_by(usr_id=usr_id, movie_id=movie_id, love=1).first()
        if isExit is not None:              # 已经收藏了
            movieInfo_dict["stared"] = 1

    return ops_renderJSON(msg="", data=movieInfo_dict)



'''
# 函数：   allMovies_getComment
# 功能：   获取该电影的相关评论
# 地址：   /getComment
# 参数：   强制参数 movie_id
#          /getComment/44  44是一个电影的id
# 传递方式 post/get         
# 返回：   标准响应：code=200, msg="movie comments", data={"commentList" : commentList}
#          错误 code=-1, msg="no such movie"
#          key: "usr_id", "time", "movie_id", "content", "head_pic", "nickname"
'''
@allMovies_blueprint_page.route("/getComment/<movie_id>", methods=["GET", "POST"])
def allMovies_getComment(movie_id):
    # 请求参数
    req = request.values
    # 电影是否存在
    movie_exit = db_mysql.session.query(Movie.movie_id).filter(Movie.movie_id == movie_id).first()
    if movie_exit is None:
        return ops_renderErrJSON(msg="no such movie")

    # 取得评论 Comment.usr_id, Comment.time, Comment.movie_id, Comment.content
    comment_query = db_mysql.session.query(Comment.usr_id, Comment.time, Comment.movie_id, Comment.content).\
        filter(Comment.movie_id == movie_id).all()
    # user_info = User.query.filter_by(usr_id=auth_info[1]).first()

    colum_names = ["usr_id", "time", "movie_id", "content"]
    # 处理
    comment_dict = {}
    if comment_query is not None:
        for i in range(len(comment_query)):                     # 对每条评论
            tmp_dict = {}
            for j in range(len(comment_query[i])):              # 形成评论项
                tmp_dict[colum_names[j]] = comment_query[i][j]
            # 拼接用户信息 "head_pic", "nickname"
            usr_id = comment_query[i][0]
            usr_query = User.query.filter(User.usr_id == usr_id).first()
            tmp_dict["nickname"] = usr_query.nickname
            tmp_dict["head_pic"] = usr_query.head_pic
            comment_dict[str(i)] = tmp_dict

    # 需要对datetime对象字符串化，否则 json会显示成 "Wed, 13 May 2020 23:12:26 GMT"
    for i in range(len(comment_dict)):
        comment_dict[str(i)]["time"] = str(comment_dict[str(i)]["time"])
        print(comment_dict[str(i)]["time"] )
    # 返回
    return_dict = {"commentList" : comment_dict}

    return ops_renderJSON(msg="success", data=return_dict)


'''
# 函数：   allMovies_postUpComment
# 功能：   上传新的评论； ！1 秒内不允许上传评论，控制频率
# 地址：   /postUpComment
# 参数：   movie_id, commentContent=评论内容  
# 传递方式 post         
# 返回：   标准响应：code=200, msg="success", data={"comment" : commentContent}
#          错误：code=-1, msg=error_msg, data={}
# #             error_msg
# #             { 0 = ok, 1:未登录, 2:评论超过长度300, 3:缺少参数movie_id, 4:缺少评论内容
#                 5 = no such movie  } 
#               error_msg 是一条字符串，是上面的某一条。不会出现多条
#
'''
@allMovies_blueprint_page.route("/postUpComment", methods=["GET", "POST"])
def allMovies_postUpComment():
    # 请求参数
    req = request.values
    error_msg = ""
    movie_id = ""
    commentContent = ""
    if "movie_id" in req:
        movie_id = req["movie_id"]
    else:
        error_msg = "缺少参数movie_id"

    if "commentContent" in req:
        commentContent = req["commentContent"]
    else:
        error_msg = "缺少评论内容"
    # 错误信息返回
    if error_msg != "":
        return ops_renderErrJSON(msg=error_msg)

    # 电影是否存在
    movie_exit = db_mysql.session.query(Movie.movie_id).filter(Movie.movie_id == movie_id).first()
    if movie_exit is None:
        return ops_renderErrJSON(msg="no such movie")

    # 处理评论内容
    if len(commentContent) > 300:
        return ops_renderErrJSON(msg="评论长度超过300")

    # 长达 连续20个（数字或字母）
    commentContent = invalidWord(commentContent)
    # 读取usr_id, 产生 time
    usr_info = g.current_user
    usr_id = usr_info.usr_id
    time = getCurrentTime()                     # 年月日 时分秒
    # 提交数据库
    model_comment = Comment(usr_id=usr_id, time=time, movie_id=movie_id, content=commentContent)
    db_mysql.session.add(model_comment)
    db_mysql.session.commit()

    # 修改评论数量
    movie_model = Movie.query.filter(Movie.movie_id == movie_id).first()
    movie_model.comment_count += 1
    db_mysql.session.add(movie_model)
    db_mysql.session.commit()
    return ops_renderJSON(msg="success", data={"comment" : commentContent})

# 函数：
# 功能：   过长的不可能单词加 "- "
## 如果一个字符串 长达连续20个（数字或字母）认为是无效的单词 此时进行截断 + "- "
def invalidWord(strIn):
    length = 0
    strNew = ""

    set_alpha = {"a", "b", "c", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q",
                 "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I",
                 "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1",
                 "2", "3", "4", "5", "6", "7", "8", "9", "0" }

    for ch in strIn:
        if ch in set_alpha:
            length += 1
        else:
            length = 0

        if length >= 20:
            strNew += "- "
            length = 0
        strNew += ch

    return strNew


'''
# 函数：   allMovies_randomOne
# 功能：   随机得到一个电影 movie_id
# 地址：   /randomOne
# 参数：   
# 传递方式 post/get         
# 返回：   标准响应：code=200, msg="success, data={"movie_id" : movie_id}
#          错误 code=-1, msg=""
#          
# 
'''
@allMovies_blueprint_page.route("/randomOne", methods=["GET", "POST"])
def allMovies_randomOne():
    # 电影总数
    query_num = db_mysql.session.query(func.count(Movie.movie_id)).scalar()

    # 随机一个
    import random
    unvalid = True
    movie_id = 1
    maxTime = 20
    while unvalid and maxTime > 0:
        movie_id = random.randint(1, query_num)
        if Movie.query.filter_by(movie_id=movie_id).first() is not None:
            unvalid = False
        maxTime -= 1

    return ops_renderJSON(msg="success", data={"movie_id" : movie_id})



'''
# 函数：   allMovies_carousel
# 功能：   返回5个轮播大图
# 地址：   /carousel
# 参数：   无
# 传递方式 post/get         
# 返回：   标准响应：code=200, msg="success", data={"moive_id":moive_id, "name":name, "huge_pic":huge_pic}
#          错误 code=-1, msg=""
#          
'''
@allMovies_blueprint_page.route("/carousel", methods=["GET", "POST"])
def allMovies_carousel():
    # 更新 carousel
    allMovies_carouselUpdate()
    # 从 carousel表 返回最新的5张海报
    from common.model.carousel import Carousel
    carousel_query = db_mysql.session.query(Carousel.movie_id, Carousel.name, Carousel.huge_pic).\
        filter(Carousel.movie_id != 1).order_by(Carousel.carousel_id.desc())[0:5]
    colum_names = ["movie_id", "name", "huge_pic"]

    # 形成dict
    carousel_dict = JsonHelper.json_sqlAlchemy_list(carousel_query, colum_names)
    # print(carousel_query)
    print(carousel_dict)
    # return "1"
    return ops_renderJSON(msg="success", data=carousel_dict)


'''
函数：     
功能：  更新carousel表，找到movies 中对应的 movie_id
'''
def allMovies_carouselUpdate():
    from common.model.carousel import Carousel
    # 找到还没有更新movie_id 的
    carousel_query = db_mysql.session.query(Carousel.name).filter(Carousel.movie_id == 1).all()
    colum_names = ["movie_id", "name", "huge_pic"]

    # 查找movies中是否有该电影
    for iterm in carousel_query:
        movies_id = db_mysql.session.query(Movie.movie_id).\
            filter(or_(Movie.name.like("%#%".replace("#", iterm[0])),
                       Movie.other_name.like("%#%".replace("#", iterm[0])) )).first()

        # 找到了则更新 carousel
        if movies_id is not None:
            carousel_update = Carousel.query.filter(Carousel.name == iterm[0]).first()
            carousel_update.movie_id = movies_id

            db_mysql.session.add(carousel_update)
            db_mysql.session.commit()


