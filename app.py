#!/usr/bin/python python3
# coding=utf-8
"""
Author: waterfall
Date: 2021-09-25 00:28:57
LastEditTime: 2021-09-25 01:42:06
Description: 项目启动文件
"""
from app import create_app, db
from app.models import User
from flask_migrate import Migrate
import os

app = create_app(os.environ.get('CONFIG', 'DevelopmentConfig'))
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username="admin").first():
            """如果没有管理员账号就新建一个"""
            user = User(username='admin', email='admin@admin.com', password="admin")
            db.session.add(user)
            db.session.commit()

    app.run(host='0.0.0.0', port='9000', debug=True)
