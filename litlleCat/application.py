#coding=utf-8
# 全局变量模块

from flask import Flask

from flask_script import Manager
# Command
from flask_script import Server
# DB
from flask_sqlalchemy import SQLAlchemy
# os
import os


# flask 对象 使用flask必须的对象
app_fk = Flask(__name__)

# manager  启动管理器，
# 包括通过命令行 参数来启动不同的任务
manager = Manager(app_fk)   # 启动管理器 和 app_fk 相关联
# 添加命令
#   这条命令需要对server操作，引入Server
manager.add_command("runserver", Server(host="0.0.0.0", use_debugger=True, use_reloader=True))


# 调度分离
# 只通过 command来调用就可以分开了
# Run_job 是统一的job入口
# 任务调度命令指向的函数
from pachong.launcher import Run_job
manager.add_command("runJob", Run_job)


# 通过配置文件 载入配置
# 默认载入基本配置
app_fk.config.from_pyfile("config/base_setting.py")
# 通过设置当前机器的 工作环境： ops_config = local | production
# Linux export; window set
if "ops_config" in os.environ:      # 根据环境加载不同的配置文件
    app_fk.config.from_pyfile("config/%s_setting.py" % (os.environ["ops_config"]))


# 数据库对象
db_mysql = SQLAlchemy(app_fk)

# 注册全局函数
# 将Flask应用代码中定义的函数，通过”add_template_global”将其传入模板即可
from common.lib.UrlManager import UrlManager
app_fk.add_template_global(UrlManager.buildUrl)
app_fk.add_template_global(UrlManager.buildStaticUrl)

