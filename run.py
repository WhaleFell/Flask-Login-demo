#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-25 00:28:57
LastEditTime: 2021-09-25 01:42:06
Description: 项目启动文件
"""
from app import create_app, db
from flask_migrate import Migrate

app = create_app('DevelopmentConfig')
migrate = Migrate(app, db)


# @app.shell_context_processors
# def make_shell_context():
#     """shell上下文"""
#     return dict(db=db, User=User)
