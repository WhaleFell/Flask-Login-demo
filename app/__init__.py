#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-25 00:52:31
LastEditTime: 2021-09-25 01:11:11
Description: Flask 应用初始化(工厂函数)
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_moment import Moment
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 登录的端点
pagedown = PageDown()
moment = Moment()


def create_app(config_name):
    """工厂函数,指定一个配置类型"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)  # 调用静态方法初始化组件

    # 注册组件
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    moment.init_app(app)

    # 注册蓝图
    from .auth import auth
    app.register_blueprint(auth)

    from .main import main
    app.register_blueprint(main)

    from .msg import msg
    app.register_blueprint(msg)

    return app
