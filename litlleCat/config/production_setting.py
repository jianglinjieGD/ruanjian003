


from config.base_setting import *
# 把base的全部引进来

SQLALCHEMY_DATABASE_URI = "mysql://wang:Wang_003@120.76.59.11/ruanjian003"

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
AUTH_COOKIE_NAME = "usr_login_cookie_name"
DOMAIN = {
    "www" : "http://120.76.69.11"

}
# 直接使用80端口
# "www" : "http://120.76.69.11"
# "http://127.0.0.1：5000"
