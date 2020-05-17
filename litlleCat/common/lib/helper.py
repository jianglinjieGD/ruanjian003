# -*- coding: utf-8 -*-
# 这里是 发送一些提示信息的函数，如 操作的成功失败等
from flask import jsonify, g , render_template, json


# 将变量数据写入 html
def ops_render(template, context={}):
    if 'current_user' in g:         # g 是flask自带的全局变量，一次访问有效
        context['current_user'] = g.current_user
    return render_template(template, **context)


def ops_renderJSON( code=200, msg="操作成功~~", data={} ):
    resp = { "code": code, "msg": msg, "data": data }
    # resp = JsonHelper.json_dict(resp)
    return jsonify( resp)


def ops_renderErrJSON( msg="系统繁忙，请稍后再试~~", data={} ):
    return ops_renderJSON( code=-1, msg=msg, data=data )



# 经过下面函数的处理， 返回json
class JsonHelper:

    # 把数据库里来的 类似list的str 转化成 list
    @staticmethod
    def str_to_list(strIn):
        if strIn is None:
            return None
        # str = ["http://gif-china.cc/uploads/allimg/202003/1d2dd4f9979b2755.jpg?h=250", "sdfsdasf"]
        # 去掉[,]
        str_splite = strIn.replace("[", "").replace("]", "").replace("\"", "").split(",")
        if str_splite is None:
            return None
        # 返回的list
        list_return = []
        for iterm in str_splite:
            list_return.append(iterm)     # 去掉 "

        return list_return

    # 读取查询返回的列表，组装成 json返回
    # 需要参数： 查询返回的列表， 每一列的列名
    @staticmethod
    def json_sqlAlchemy_list(sqlAlchemy_list, colums_name):
        movies_json = []
        for item in sqlAlchemy_list:
            tmp_json = {}
            for i in range(len(colums_name)):
                tmp_json[colums_name[i]] = item[i]          # 用列名作为key
            movies_json.append(tmp_json)                    # 以movie_id作为key； 电源信息的dict作为value

        return movies_json
        # return json.dumps( movies_json, ensure_ascii=False )

    # 对电影详情信息 转化成 dict
    @staticmethod
    def list_to_dict(keys, values):
        return_dict = {}
        if len(keys) != len(values):
            return None
        for i in range(len(keys)):
            return_dict[str(keys[i])] = values[i]

        return return_dict

    # 返回对字典进行json化
    @staticmethod
    def json_dict(dict_in):
        # return json.dumps(dict_in, ensure_ascii = False )
        return dict_in


'''
def iPagenation( params):
    total_count = int( params['total_count'] )
    page_size = int( params['page_size'] )
    page = int( params['page'] )

    total_pages = math.ceil(total_count / page_size)
    total_pages = total_pages if total_pages > 0 else 1

    is_prev = 0 if page <= 1 else 1
    is_next = 0 if page >= total_pages else 1
    pages = {
        'current':page,
        'total_pages':total_pages,
        'total':total_count,
        'page_size':page_size,
        'is_next': is_next,
        'is_prev': is_prev,
        'range': range( 1,total_pages + 1 ),
        'url':params['url']
    }
    return pages
   
'''