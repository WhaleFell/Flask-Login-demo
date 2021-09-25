#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-25 01:34:33
LastEditTime: 2021-09-25 01:35:39
Description: 登录蓝图
"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
