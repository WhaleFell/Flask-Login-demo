#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-25 01:25:55
LastEditTime: 2021-09-25 01:36:49
Description: 主蓝图-视图文件
"""
from . import main
from flask import render_template


@main.route('/')
def index():
    return render_template('index.html')
