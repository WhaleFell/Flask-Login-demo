#!/usr/bin/python python3
# coding=utf-8
'''
Author: whalefall
Date: 2021-09-25 01:25:00
LastEditTime: 2021-09-25 01:28:28
Description: 主蓝图
'''
from flask import Blueprint

main = Blueprint('main',__name__)

from . import errors,views


