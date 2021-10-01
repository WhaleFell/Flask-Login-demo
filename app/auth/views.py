#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-09-25 01:35:12
LastEditTime: 2021-09-25 01:36:41
Description: 登录蓝图-视图函数
"""
from . import auth
from flask import render_template, flash, redirect, url_for, session, request
from .forms import LoginForm, RegForm
from ..models import User, db
from flask_login import current_user, login_user, login_required, logout_user


@auth.route('/index/')
@login_required
def login_index():
    """登录后显示的视图"""
    return render_template('auth/KsLoginSuccessAction.html', current_user=current_user)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """登录视图函数"""
    form = LoginForm()
    if session.get('user') and session.get('pwd'):
        """注册后自动填充账号密码"""
        form.email.data = session.get('user')
        form.password.data = session.get('pwd')
    if form.validate_on_submit():
        print('提交表单')
        """支持邮箱和用户名登录"""
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User.query.filter_by(username=form.email.data).first()
            if user is None:
                flash("用户不存在!")
            elif user.validate_pwd_username(form.password.data):
                print(f"用户{user.username}登录成功!")
                login_user(user, remember=form.remember_me.data)
                next = request.args.get('next')
                # 链接中有参数则跳转
                if next:
                    return redirect(next)
                else:
                    return redirect(url_for('auth.login_index'))
            else:
                flash("登录失败,请检查(用户名)账号密码!")
                # 使用重定向才不会莫名弹出警告
                return redirect(url_for('auth.login'))

        elif user.validate_pwd_email(form.password.data):
            print(f"用户{user.username}登录成功!")
            login_user(user, remember=form.remember_me.data)
            next = request.args.get('next')
            # 链接中有参数则跳转
            if next:
                return redirect(next)
            else:
                return redirect(url_for('auth.login_index'))
        else:
            flash("登录失败,请检查(邮箱)账号密码!")
            # 使用重定向才不会莫名弹出警告
            return redirect(url_for('auth.login'))
    return render_template('auth/KsLoginAction.html', form=form)


@auth.route('/reg/', methods=['GET', 'POST'])
def reg():
    """注册视图函数"""
    form = RegForm()
    next = request.args.get('next')
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("账号注册成功!请登录")
        session['user'] = form.username.data
        session['pwd'] = form.password.data
        if next:
            return redirect(url_for('auth.login', next=next))
        else:
            return redirect(url_for('auth.login'))
    return render_template('auth/KsLoginReg.html', form=form)


@auth.route('/logout/', methods=['GET', 'POST'])
def logout():
    """登出用户"""
    if current_user.is_authenticated:
        flash(f"用户{current_user.username}已登出")
        logout_user()
    else:
        flash("没有登录任何用户")
    next = request.args.get('next')
    # 链接中有参数则跳转
    if next:
        return redirect(next)
    else:
        return redirect(url_for('auth.login'))
