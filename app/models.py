#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-25 01:23:11
LastEditTime: 2021-09-25 01:39:28
Description: 数据库模型文件
"""
import random
import string

from . import db
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from markdown import markdown


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
    # 一的那端,一个用户对应多条评论;
    # 第一个参数:关系另一端的模型
    # backref:向Msg模型添加一个author属性,通过Msg.author就可以获取到对应的单个User模型对象
    msgs = db.relationship('Msg', backref='author')

    def validate_pwd_email(self, pwd):
        """用邮箱验证密码"""
        if User.query.filter_by(email=self.email).first().password == pwd:
            return True
        else:
            return False

    def validate_pwd_username(self, pwd):
        """用用户名验证密码"""
        if User.query.filter_by(username=self.username).first().password == pwd:
            return True
        else:
            return False


class Msg(db.Model):
    """留言数据库模型"""
    __tablename__ = 'msgs'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 一个用户对应多条留言(一对多关系)[多的一端]
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 游客允许空数值
    looker_id = db.Column(db.Integer, db.ForeignKey('lookers.id'), nullable=True)

    @staticmethod
    def on_changer_body(target, value, oldvalue, init):
        """定义一个函数用于触发事件将md转换成html的回调函数
        target: 数据库对象,可进行修改
        value: 监听字段修改后的值
        oldvalue: 监听字段修改前的值
        """
        if not value == oldvalue:
            target.body_html = markdown(value, output_format='html')


class Looker(db.Model):
    """游客表"""
    __tablename__ = 'lookers'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # 生成时间
    looker_name = db.Column(db.String(64), unique=True)  # 游客名
    ip = db.Column(db.String(64))  # 游客ip地址
    # 一的那端,一个游客对应多条评论;
    # 第一个参数:关系另一端的模型
    # backref:向Msg模型添加一个looker属性,通过Msg.looker就可以获取到对应的单个Looker模型对象
    msgs = db.relationship('Msg', backref='looker')

    def new_looker(self):
        """新建一个随机名称的用户对象并返回"""
        str_list = [random.choice(string.digits + string.ascii_letters) for i in range(5)]
        random_str = ''.join(str_list)
        self.looker_name = f"游客{random_str}"
        return self


# 数据库监听,一旦Msg.body被修改就调用转换方法
db.event.listen(Msg.body, 'set', Msg.on_changer_body)
