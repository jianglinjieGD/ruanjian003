# 这里是基本配置（都需要的配置）


# DEBUG = True
DEBUG = False

# SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = False
SQLALCHEMY_ECHO = True
SQLALCHEMY_ENCODING = "utf-8mb4"
AUTH_COOKIE_NAME = "usr_login_cookie_name"
# SQLALCHEMY_DATABASE_URI = "mysql://root:mysql003@127.0.0.1/mysql"
SQLALCHEMY_DATABASE_URI = "mysql://wang:Wang_003@120.76.59.11/ruanjian003"

LOGIN_REQUIREMENT_LIST = ["postUpComment", "postUpComment", "myComment", "deleteMyComment",
                          "myLove", "deleteMyLove", "addLove", "setHeadPic", "setNickname",
                          "myCommentMovie"]


AUTH_COOKIE_NAME = "usr_login_cookie_name"
DOMAIN = {
    "www" : "http://120.76.69.11"

}
# 直接使用80端口
# "www" : "http://120.76.69.11"
# "http://127.0.0.1：5000"


