#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-25 01:23:11
LastEditTime: 2021-09-25 01:39:28
Description: 数据库模型文件
"""
from . import db
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    """获取已登录用户的信息,返回一个用户对象"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """用户数据库对象模型"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))

    def validate_pwd_email(self, pwd):
        if User.query.filter_by(email=self.email).first().password == pwd:
            return True
        else:
            return False

    def validate_pwd_username(self, pwd):
        if User.query.filter_by(username=self.username).first().password == pwd:
            return True
        else:
            return False
