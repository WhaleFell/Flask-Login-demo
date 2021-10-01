from . import msg
from flask import render_template, request
from .forms import MsgForm
from ..models import Msg, db
from flask_login import current_user
from flask import redirect, url_for


@msg.route('/msg/', methods=['GET', 'POST'])
def msg_index():
    """留言板"""
    form = MsgForm()
    # 在无法把page参数转化为int是使用默认值
    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        # _get_current_object() 获取真正的用户对象
        msg = Msg(body=form.body.data, author=current_user._get_current_object())
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('msg.msg_index'))
    # 以时间戳降序排列(降序关键字desc)
    # paginate(当前页数,每页显示的数据数,超出页数时是否返回404)
    pagination = Msg.query.order_by(Msg.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    msgs = pagination.items  # 当前页面的记录
    return render_template('msg/index.html', form=form, msgs=msgs, pagination=pagination)
