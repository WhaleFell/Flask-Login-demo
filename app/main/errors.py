#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-09-25 01:25:27
LastEditTime: 2021-09-25 01:31:31
Description: 主蓝图-错误处理
'''
from . import main
from flask import render_template


@main.app_errorhandler(404)
def page_not_found(e):
    """处理404错误"""
    return render_template('error.html', e=e, title='页面找不到了')


@main.app_errorhandler(500)
def service_error():
    """处理500服务器错误"""
    return render_template('error.html', e=e, title='服务器内部错误')
