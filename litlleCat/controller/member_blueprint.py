# 用户登录、登出、注册
from flask import Blueprint, request, make_response, json, redirect, g
from common.lib.helper import ops_renderErrJSON, ops_renderJSON, ops_render, JsonHelper
from common.model.users import User
from common.lib.UserService import UserService
from common.lib.DataHelper import getCurrentTime
from application import db_mysql, app_fk
from common.lib.UrlManager import UrlManager
from common.model.comment import Comment
from common.model.history import History
from common.model.movies import Movie

from sqlalchemy import or_,and_

member_blueprint_page = Blueprint("member_blueprint_page", __name__)

'''
# 函数：   usr_reg
# 功能：   接收注册信息，进行注册或者返回错误信息
# 地址：   usr/reg
# 参数：   login_name login_pwd login_pwd2
# 传递方式 post         
# 返回：   标准响应：code=200, msg="success", data={}
#          错误：code=-1, msg="error", data={"序号": error_msg}   
#          这里的错误可以有多个同时存在， 序号不绑定：1和 "请使用post"不是绑定的
#          error_msg
#          1:请使用post, 2:请输入正确的登录名！,3:用户名已存在！, 4:密码至少要6个字符哦！, 
#          5:两次输入的密码不同呢！ 
# 例子：   {code=-1, msg="error", data={"1":"请使用post", "2":"请输入正确的登录名",......} }               
'''
@member_blueprint_page.route("/reg", methods=["GET", "POST"])
def usr_reg():
    # 接收用户的注册请求信息
    error_list = []
    if request.method == "GET":
        error_list.append("请使用post")

    if len(error_list) < 1:
        # 接收参数信息
        regValues = request.values
        login_name = regValues["login_name"] if "login_name" in regValues else ""
        login_pwd = regValues["login_pwd"] if "login_pwd" in regValues else ""
        login_pwd2 = regValues["login_pwd2"] if "login_pwd2" in regValues else ""
        # 确定信息合法
        if login_name is None or len(login_name) < 1:
            error_list.append("请输入正确的登录名！")
        if login_pwd is None or len(login_pwd) < 6:
            error_list.append("密码至少要6个字符哦！")
        if login_pwd2 is None or len(login_pwd2) < 6:
            error_list.append("密码至少要6个字符哦！")
        if login_pwd != login_pwd2:
            error_list.append("两次输入的密码不同呢！")

        # 用户名是否已存在
        usrInfo_name = User.query.filter_by( login_name = login_name).first()
        if usrInfo_name is not None:
            error_list.append("用户名已存在！")
    if len(error_list) < 1:
        # 生成salt、 saltKey
        salt = UserService.genSalt()
        saltKey = UserService.genePwd(login_pwd, salt)
        print("%s---%s" % (salt, saltKey) )
        # 生成createTime、 updateTime 等
        model_usr = User()
        model_usr.login_name = login_name
        model_usr.nickname = regValues["nick_name"] if "nick_name" in regValues else login_name
        model_usr.login_pwd = saltKey
        model_usr.login_salt = salt
        model_usr.created_time = model_usr.updated_time = getCurrentTime()      # "%Y-%M-%D %H:%M:%S"
        # 其他保持默认

        # 存入数据库
        # 通过数据库的session 添加模型，并且更新到数据库
        db_mysql.session.add(model_usr)
        db_mysql.session.commit()
    # 返回信息
    msg = "error"
    code = -1
    error_dict = {}
    for i in range(len(error_list)):
        error_dict[str(i)] = error_list[i]

    if len(error_list) < 1:
        code = 200
        msg = "success"

    return ops_renderJSON(code=code, msg=msg, data={"error_list" : error_list})


'''
# 函数：   usr_login
# 功能：   用户登录
# 地址：   usr/login
# 参数：   login_name login_pwd 
# 传递方式 post         
# 返回：   标准响应：code=200, msg="success", data={}
#          错误：code=-1, msg=error_msg, data={}   
#          error_msg
#          0:登录成功 1: 请使用post; 2:请输入正确的登录名; 3:请输入正确的密码; 4:账号和密码不匹配
#          5:账号被禁用，请联系管理员;
#           
#          
'''
@member_blueprint_page.route("/login", methods=["GET", "POST"])
def usr_login():
    # 初始化 操作状态和标记信息
    error_flg = 1
    error_msg = ""
    # 请求类型
    if request.method != "POST":
        error_flg = "请使用post"
    else:
        error_flg += 1
    # 读取请求信息
    regValues = request.values
    login_name = regValues["login_name"] if "login_name" in regValues else ""
    login_pwd = regValues["login_pwd"] if "login_pwd" in regValues else ""
    # 用户名格式
    if error_flg == 2:
        if login_name is None or len(login_name) < 1:
            error_msg = "请输入正确的登录名"
        else:
            error_flg += 1
    # 用户密码格式
    if error_flg == 3:
        if login_pwd is None or len(login_pwd) < 6:
            error_msg = "请输入正确的密码"
        else:
            error_flg += 1
    # 验证密码和账户
    if error_flg == 4:
        usrInfo = User.query.filter_by(login_name=login_name).first()
        # 用户名不存在 或 不匹配密码
        if not usrInfo or usrInfo.login_pwd != UserService.genePwd(login_pwd, usrInfo.login_salt):
            error_msg = "账号和密码不匹配"
        else:
            error_flg += 1
    # 账号状态
    if error_flg == 5:
        if usrInfo.status != 1:
            error_msg = "账号被禁用，请联系管理员"
        else:
            error_flg += 1

    # 成功登录
    response = ops_renderJSON(code=-1, msg=error_flg, data={"error_msg": error_msg})
    if error_flg == 6:
        error_flg = 0
        error_msg = "登录成功"
        response = ops_renderJSON(msg=error_flg, data={"error_msg": error_msg})
        response.set_cookie(app_fk.config['AUTH_COOKIE_NAME'],
                            "%s#%s" % (UserService.geneAuthCode(usrInfo), usrInfo.usr_id), 60 * 60 * 24 * 120)
    # cookie(name = app_fk.config['AUTH_COOKIE_NAME'],
    # value = md5混合多个信息加密的md5字段#用户id， 保存时间)

    return response


'''
# 函数：   usr_logout
# 功能：   用户登出
# 地址：   usr/logout
# 参数：   无
# 传递方式 post         
# 返回：   标准响应：code=200, msg="success", data={}
#          错误：code=-1, msg=error_msg, data={}   
#          还没想到错误的情况
#          
'''
@member_blueprint_page.route("/logout", methods=["GET", "POST"])
def usr_logout():
    # 跳转到主页
    response = ops_renderJSON(msg="logout")
    # response = make_response(redirect(UrlManager.buildUrl("/")))
    # 删除 cookie即可
    response.delete_cookie(app_fk.config['AUTH_COOKIE_NAME'])

    return response



'''
# 函数：   usr_myComment
# 功能：   用户查看已评论
# 地址：   usr/myComment
# 参数：   无
# 传递方式 post         
# 返回：   标准响应：code=200, msg="my comments", data={"commentList" : commentList}
#          错误 code=-1, msg="" 未想到
#          key: "usr_id", "time", "movie_id", "content", "head_pic", "nickname"
# #          "commentList":{ "1": { "time":xx, "movie_id":xx, "content":text}
#                            "2": {......}
# #           }
#          相比电影的评论列表， 省略了 urs_id 
#          未登录除外，未登录是统一处理的
'''
@member_blueprint_page.route("/myComment" , methods=["GET", "POST"])
def usr_myComment():
    # 从cookie读取用户信息
    usr_info = g.current_user
    usr_id = usr_info.usr_id
    app_fk.logger.info("usr_id: "+ str(usr_id))
    # 根据usr_id 获取所有相关的评论
    comment_query = db_mysql.session.query(Comment.movie_id, Comment.time, Comment.content).\
        filter(Comment.usr_id == usr_id).all()
    colum_names = ["movie_id", "time" , "content"]

    # 处理成dict
    comment_dict = {}
    for i in range(len(comment_query)):
        tmp_dict = {}
        for j in range(len(comment_query[i])):
            tmp_dict[colum_names[j]] = comment_query[i][j]
        comment_dict[str(i)] = tmp_dict

    # 需要对datetime对象字符串化，否则 json会显示成 "Wed, 13 May 2020 23:12:26 GMT"
    # 这和数据库的显示不匹配，造成不必要的麻烦
    for i in range(len(comment_dict)):
        comment_dict[str(i)]["time"] = str(comment_dict[str(i)]["time"])
        print(comment_dict[str(i)]["time"])

    return ops_renderJSON(msg="my comments", data={"commentList" : comment_dict})

'''
# 函数：   usr_deleteMyComment
# 功能：   删除已评论
# 地址：   usr/deleteMyComment
# 参数：   强制 time; 查看我的评论处获取到的 time
#		   if time == "all" : will delete all comments from this user
#          usr/deleteMyComment/时间或者all
#
# 传递方式 post         
# 返回：   标准响应：code=200, msg="success", data={}
#          错误： 缺少 time 参数会 404
#          错误：code=-1, msg="no such comment", data={}   
'''
@member_blueprint_page.route("/deleteMyComment/<time>" , methods=["GET", "POST"])
def usr_deleteMyComment(time):
    # 通过 usr_id 和 time 删除相应的评论
    # 从cookie读取用户信息
    usr_info = g.current_user
    usr_id = usr_info.usr_id
    movie_id = ""
    # 操作数据库
    time = time.replace("\"", "")               # 去掉引号 如果有


    if time != "all":
        comment_model = Comment.query.filter_by(usr_id=usr_id, time=time).first()
        if comment_model is None:
            return ops_renderErrJSON(msg="没有这条评论")
        # 删除单条评论
        db_mysql.session.delete(comment_model)
        db_mysql.session.commit()
        movie_id = comment_model.movie_id
    else:   # 删除全部评论
        comment_model = Comment.query.filter_by(usr_id=usr_id).all()
        movie_id = comment_model[0].movie_id
        # 操作数据库
        for h_q in comment_model:
            db_mysql.session.delete(h_q)
            db_mysql.session.commit()

    # 修改评论数量
    comment_count_now = Comment.query.filter(Comment.movie_id == movie_id).count()      # 评论数量
    movie_model = Movie.query.filter(Movie.movie_id == movie_id).first()
    movie_model.comment_count = comment_count_now
    db_mysql.session.add(movie_model)
    db_mysql.session.commit()

    # 返回 提示信息
    return ops_renderJSON(msg="success")



'''
# 函数：   usr_myLove
# 功能：   用户查看收藏
# 地址：   usr/myLove
# 参数：   无
# 传递方式 post         
# 返回：   标准响应：code=200, msg="success", data=movieList
#          错误：code=-1, msg="" 未想到 
# #        key_name = ["movie_id", "name", "cover_pic","comment_count","douban_score", "classification"]
#          和全部分类页 返回的电影列表相同
#           
'''
@member_blueprint_page.route("/myLove" , methods=["GET", "POST"])
def usr_myLove():
    # 从cookie读取用户信息
    usr_info = g.current_user
    usr_id = usr_info.usr_id
    # id 搜索love 的movie_id ==> list
    history_query = db_mysql.session.query(History.movie_id).filter(History.usr_id==usr_id, History.love==1).all()
    # movie_id  ==> movie simple info
    movie_query = db_mysql.session.query(Movie.movie_id, Movie.name, Movie.cover_pic, Movie.comment_count,
                                         Movie.douban_score, Movie.classification).\
        filter(Movie.movie_id.in_(history_query)).all()
    colum_names = ["movie_id", "name", "cover_pic", "comment_count", "douban_score", "classification"]
    # 利用colum_names + movie_query 形成字典
    movie_sampleInfo = JsonHelper.json_sqlAlchemy_list(movie_query, colum_names)

    return ops_renderJSON(msg="success", data=movie_sampleInfo)


'''
# 函数：   usr_addLove
# 功能：   用户添加某条收藏
# 地址：   usr/addLove
# 参数：   强制参数 movie_id
# 示例：   usr/addLove/44    44 是一个电影的id		   
# 传递方式 post         
# 返回：   标准响应：code=200, msg="success", data={}
#          错误：without movie_id: 确实该参数 会404
#          错误：code=-1, msg="no such movie", data={}   
#          错误：code=-1, msg="this love-movie is exit", data={} 
'''
@member_blueprint_page.route("/addLove/<movie_id>" , methods=["GET", "POST"])
def usr_addLove(movie_id):
    # 从cookie读取用户信息
    usr_info = g.current_user
    usr_id = usr_info.usr_id

    # 电影是否存在
    movie_exit = db_mysql.session.query(Movie.movie_id).filter(Movie.movie_id == movie_id).first()
    if movie_exit is None:
        return ops_renderErrJSON(msg="no such movie")

    # 是否已经收藏
    isExit = History.query.filter_by(usr_id=usr_id, movie_id=movie_id, love=1).first()
    if isExit is not None:
        return ops_renderErrJSON(msg="this love-movie is exit")

    # 写入数据库 History
    history_query = History(usr_id=usr_id, movie_id=movie_id, love=1, isHistory=0)
    db_mysql.session.add(history_query)
    db_mysql.session.commit()

    # 修改收藏数量
    love_count_now = History.query.filter(History.movie_id == movie_id).count()  # 收藏 数量
    movie_model = Movie.query.filter(Movie.movie_id == movie_id).first()
    movie_model.love_count = love_count_now
    db_mysql.session.add(movie_model)
    db_mysql.session.commit()

    return ops_renderJSON( msg="success")



'''
# 函数：   usr_deleteMyLove
# 功能：   用户删除某条收藏
# 地址：   usr/deleteMyLove
# 参数：   强制参数 movie_id
#		   if movie_id == "all" : 删除该用户的全部收藏
# 示例：   usr/addLove/44    44 是一个电影的id		 
# 传递方式 post         
# 返回：   标准响应：code=200, msg="success", data={}
#          错误：code=-1, msg="no such movie", data={}   
'''
@member_blueprint_page.route("/deleteMyLove/<movie_id>" , methods=["GET", "POST"])
def usr_deleteMyLove(movie_id):
    # 从cookie读取用户信息
    usr_info = g.current_user
    usr_id = usr_info.usr_id
    # 读取请求
    req = request.values

    if movie_id != "all":
        # 电影是否存在
        movie_exit = db_mysql.session.query(Movie.movie_id).filter(Movie.movie_id == movie_id).first()
        if movie_exit is None:
            return ops_renderErrJSON(msg="no such movie")
        # 查数据库 History
        history_query = History.query.filter_by(usr_id=usr_id, movie_id=movie_id).first()
        # 是否有收藏
        if history_query is None:
            return ops_renderErrJSON(msg="未收藏该电影")
        # 删除单条收藏
        db_mysql.session.delete(history_query)
        db_mysql.session.commit()
    else:
        # if movie_id == "all" 删除所有收藏
        history_query = History.query.filter_by(usr_id=usr_id).all()
        # 操作数据库 删除多条收藏
        for h_q in history_query:
            db_mysql.session.delete(h_q)
            db_mysql.session.commit()

    # 修改收藏数量
    love_count_now = History.query.filter(History.movie_id == movie_id).count()  # 收藏 数量
    movie_model = Movie.query.filter(Movie.movie_id == movie_id).first()
    movie_model.love_count = love_count_now
    db_mysql.session.add(movie_model)
    db_mysql.session.commit()

    return ops_renderJSON(msg="success")

