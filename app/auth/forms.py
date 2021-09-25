from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError  # 验证失败抛出异常
from ..models import User


class LoginForm(FlaskForm):
    """登录表单类"""
    email = StringField('邮箱or用户名:', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码:', validators=[DataRequired()])
    remember_me = BooleanField('保持登录?')
    submit = SubmitField('登录')


class RegForm(FlaskForm):
    """注册表单类"""
    email = StringField('邮箱:', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名:', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码:', validators=[DataRequired(), EqualTo("password2", message='两次输入的密码不一致!')])
    password2 = PasswordField('再次输入密码:', validators=[DataRequired()])
    submit = SubmitField('注册')

    # 校验邮箱和用户名是否有重复,表格对象为第二个参数
    # 两个自定义验证函数格式: `validate_表格字段名`
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            field.data = ''
            raise ValidationError('邮箱已存在!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            field.data = ''
            raise ValidationError('用户名已存在!')
