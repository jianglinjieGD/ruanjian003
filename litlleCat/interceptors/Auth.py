# -*- coding: utf-8 -*-
# interceptor： 拦截器
# Auth： 验证
from application import app_fk
from flask import request, g
from common.model.users import User
from common.lib.UserService import UserService



'''
# 函数：   before_request
# 功能：   需要登录时会拦截未登录的请求； 以及其他关键词
# 地址：   无，所以请求都会经过此函数
# 参数：   无
      
# 返回：   需要登录而没有登陆： “请登录”
'''
@app_fk.before_request
def before_request():
    app_fk.logger.info( "--------before_request--------" )
    # 要求登录的关键字 list
    login_requrment_list = app_fk.config["LOGIN_REQUIREMENT_LIST"]
    # 请求的url
    url_ip = request.url

    g.current_user = None           # g是自带的，一次请求中的全局变量
    # 检查登录
    user_info = check_login()       # 检查是否登录： 登录时会保存coolie到本地
    # app_fk.logger.info(user_info)

    if user_info:
        g.current_user = user_info  # 登录则把用户信息放到全局变量g
    else:
        # 没有登录
        for item in login_requrment_list:       # 对于在 强制要求登录的列表里的
            if url_ip.find(item) != -1:         # url含有强制登录关键词则要求登录
                return "请登录"



@app_fk.after_request
def after_request( response ):
    app_fk.logger.info("--------after_request--------")
    return response


'''
# 函数：   check_login
# 功能：   判断用户是否登录
# 地址：   无
# 参数：   无
#          仅内部使用
# 返回：   用户信息（未登录为空）
'''
def check_login():
    # 获取此次请求的cookie，通过设置的cookie名字
    # 取出cookie value 来验证字段
    cookies = request.cookies

    cookie_name = app_fk.config['AUTH_COOKIE_NAME']      # 设置的cookie name
    # 需验证的cookie value字段
    auth_cookie = cookies[cookie_name] if cookie_name in cookies else None
    # check_login中 并没使用cookie的整个value去验证，那是不安全的
    if auth_cookie is None:     # 没有cookie肯定是错的
        return False
    # 提取cookie value 的字段，设置里两个字段，所以不是的话一定是错的
    auth_info = auth_cookie.split("#")
    if len( auth_info ) != 2:
        return False
    # 查id字段
    try:
        user_info = User.query.filter_by( usr_id = auth_info[1] ).first()
    except Exception :
        return False

    if user_info is None:
        return False
    # 查 验证码字段
    # 按照规则产生的验证码和此次请求的验证码字段
    if auth_info[0] != UserService.geneAuthCode( user_info ):
        return False
    # 确认无误： 返回用户信息对象

    return user_info


