# this is a file about routing
from application import app_fk
from controller.bluePrint_1 import bluePrint_1_page
from controller.member_blueprint import member_blueprint_page
from controller.allMovies_blueprint import allMovies_blueprint_page


# 注册蓝图1，前缀名是 page1
app_fk.register_blueprint(bluePrint_1_page, url_prefix="/page1")
app_fk.register_blueprint(member_blueprint_page, url_prefix="/usr")
app_fk.register_blueprint(allMovies_blueprint_page, url_prefix="/")



