from flask import Blueprint, request, make_response, jsonify
from application import db_mysql


bluePrint_1_page = Blueprint("bluePrint_1_page", __name__)    # 新建一个蓝图


@bluePrint_1_page.route("/kk")
def json_return():
    from user_autoModel import Testtable
    usr = Testtable(name="jianglinjie hahah")
    db_mysql.session.add(usr)
    db_mysql.session.commit()
    return jsonify({"msg":"for test the SQLALchemy"})


@bluePrint_1_page.route("/get")
def get():
    vals = request.values
    var_a = ""
    var_a = vals['a'] if "a" in vals else None
    return "var: %s " % var_a


@bluePrint_1_page.route("/upload", methods=["POST"])
def upload():
    file = request.files["fileName"]
    return "info: %s" % file


@bluePrint_1_page.route("/post", methods=[ "POST" ])
def post():
    vals = request.values
    var_a = ""
    var_a = vals['a'] if "a" in vals else "a is not exited"
    return "var: %s " % var_a


@bluePrint_1_page.route("/myPath/<param>")
def my_path(param):
    return "here is myPath! %s " % param


@bluePrint_1_page.route("/")
def hello():
    from application import app_fk, db_mysql
    from common.model.movie import Movie
    movies_query_list = db_mysql.session.query(Movie).get(44)

    print(movies_query_list)



