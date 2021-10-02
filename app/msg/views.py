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
        looker_name = session.get('looker_name')
        ip = request.remote_addr
        if looker_name and Looker.query.filter_by(looker_name=looker_name).first():
            # 如果session中的looker_id有且存在,更新ip
            Looker.query.filter_by(looker_name=looker_name).update({'ip': f"{ip}"})
            db.session.commit()
            author = Looker.query.filter_by(looker_name=looker_name).first()
        else:
            # fix: 弃用id命名,改为随机命名法,只有评论过的游客才会保留
            looker = Looker(ip=ip).new_looker()  # 生成游客对象但是没有提交
            author = looker

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
            db.session.add_all([msg, author])
            session['looker_name'] = author.looker_name  # session保存游客name
            db.session.commit()
            return redirect(url_for('msg.msg_index'))

    # 以时间戳降序排列(降序关键字desc)
    # paginate(当前页数,每页显示的数据数,超出页数时是否返回404)
    # print(author.looker_name)
    pagination = Msg.query.order_by(Msg.timestamp.desc()).paginate(page, per_page=10, error_out=False)
    msgs = pagination.items  # 当前页面的记录
    return render_template('msg/index.html', form=form, msgs=msgs, pagination=pagination, author=author)
