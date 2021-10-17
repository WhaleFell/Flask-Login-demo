#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-25 00:28:13
LastEditTime: 2021-09-25 00:49:33
Description: Flask 项目配置文件
"""
import os
import platform
from datetime import timedelta
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))  # 项目的绝对目录


class Config(object):
    """主配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lovehyy123456hjl'  # 密钥
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 数据库
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # 设置 session 的过期时间.
    BASEDIR = basedir

    @staticmethod
    def init_app(app):
        """静态方法,用于其他组件初始化"""
        Path.mkdir(Path(basedir, 'db'), exist_ok=True)  # 新建数据库文件夹


class DevelopmentConfig(Config):
    """开发环境,继承于Config主配置"""
    DEBUG = True
    # 判断操作系统
    if platform.system() == "Windows":
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'data.db')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'db', 'data.db')


class TencentConfig(Config):
    DEBUG = True
    # 判断操作系统
    if platform.system() == "Windows":
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('/tmp/', 'data.db')
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join('/tmp/', 'data.db')


# 开发环境选择字典
config = {
    "development": DevelopmentConfig,
    "tencent": TencentConfig
}
