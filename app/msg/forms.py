from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField


class MsgForm(FlaskForm):
    """留言板表单"""
    body = PageDownField("请输入内容(支持MarkDown语法)", validators=[Required()])
    submit = SubmitField('提交')
