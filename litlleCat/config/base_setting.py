# 这里是基本配置（都需要的配置）

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_ENCODING = "utf-8mb4"
AUTH_COOKIE_NAME = "usr_login_cookie_name"
# SQLALCHEMY_DATABASE_URI = "mysql://root:mysql003@127.0.0.1/mysql"
LOGIN_REQUIREMENT_LIST = ["postUpComment", "postUpComment", "myComment", "deleteMyComment",
                          "myLove", "deleteMyLove", "addLove"]

