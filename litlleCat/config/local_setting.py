

from config.base_setting import *
# 把base的全部引进来


SQLALCHEMY_DATABASE_URI = "mysql://root:mysql003@127.0.0.1/site_ruanjian003"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
AUTH_COOKIE_NAME = "usr_login_cookie_name"
DOMAIN = {
    "www" : "http://127.0.0.1:5000"

}
