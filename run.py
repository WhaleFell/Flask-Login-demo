#!/usr/bin/python python3
# coding=utf-8
"""
Author: waterfall
Date: 2021-09-25 00:28:57
LastEditTime: 2021-09-25 01:42:06
Description: 项目启动文件
"""
import os

import click

from app import create_app, db
from app.models import User
from flask_migrate import Migrate

app = create_app(os.environ.get('FLASK_CONFIG') or 'Development')
# 设置数据库批处理使其支持sqlite
migrate = Migrate(app, db, render_as_batch=True)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)


@app.cli.command()
def deploy():
    """初始化Flask应用运行配置"""
    with app.app_context():
        db.drop_all()  # 删除原有
        db.create_all()  # 创建数据库
        if not User.query.filter_by(username="admin").first():
            """如果没有管理员账号就新建一个"""
            user = User(username='admin',
                        email='admin@admin.com', password="admin")
            db.session.add(user)
            db.session.commit()
    click.echo('数据库初始化成功!')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port='9000', debug=True)
