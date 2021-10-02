from . import msg
from flask import render_template, request, session
from .forms import MsgForm
from ..models import Msg, db, Looker
from flask_login import current_user
from flask import redirect, url_for


@msg.route('/msg/', methods=['GET', 'POST'])
def msg_index():
    """留言板"""
    form = MsgForm()
    # 在无法把page参数转化为int是使用默认值
    page = request.args.get('page', 1, type=int)
    # 验证是否登录
    if current_user.is_authenticated:
        # _get_current_object() 获取真正的用户对象
        author = current_user._get_current_object()
    else:
        # 针对未登录的用户,即游客.
        looker_id = session.get('looker_id')
        ip = request.remote_addr
        if looker_id and Looker.query.filter_by(id=int(looker_id)).first():
            # 如果session中的looker_id有且存在
            Looker.query.filter_by(id=int(looker_id)).update({'ip': f"{ip}"})
            db.session.commit()
            author = Looker.query.filter_by(id=int(looker_id)).first()
        else:
            # TODO:这里我的实现有点傻逼了,不知道那位大佬有更好的方法.
            looker_raw = Looker(ip=ip).new_looker()  # 生成游客对象
            # print(looker_raw.id)
            # 以新生成的游客对象id字段更新looker_name
            Looker.query.filter_by(id=int(looker_raw.id)).update({'looker_name': f"游客{looker_raw.id}"})
            session['looker_id'] = looker_raw.id  # session保存游客id
            db.session.commit()  # 提交更改
            author = Looker.query.filter_by(id=int(looker_raw.id)).first()  # 读取该游客对象

    # 提交表单
    if form.validate_on_submit():
        if current_user.is_authenticated:
            # 针对已登录用户
            msg = Msg(body=form.body.data, author=author)
            db.session.add(msg)
            db.session.commit()
            return redirect(url_for('msg.msg_index'))
        else:
            # 针对游客用户
            msg = Msg(body=form.body.data, looker=author)
            db.session.add(msg)
            db.session.commit()
            return redirect(url_for('msg.msg_index'))

    # 以时间戳降序排列(降序关键字desc)
    # paginate(当前页数,每页显示的数据数,超出页数时是否返回404)
    # print(author.looker_name)
    pagination = Msg.query.order_by(Msg.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    msgs = pagination.items  # 当前页面的记录
    return render_template('msg/index.html', form=form, msgs=msgs, pagination=pagination, author=author)
