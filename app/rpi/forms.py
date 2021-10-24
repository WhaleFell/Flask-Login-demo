# -*- coding: utf-8 -*-
# @Time : 2021/10/24 15:05
# @Author : WhaleFall
# @Site : 编辑FRPC配置的表单
# @File : forms.py
# @Software: PyCharm
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField


class IniForm(FlaskForm):
    """留言板表单"""
    body = TextAreaField("请输入FRPC配置", validators=[Required()])
    submit = SubmitField('提交')
