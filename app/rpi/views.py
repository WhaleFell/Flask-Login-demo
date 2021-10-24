import traceback

from flask import render_template, request, make_response, current_app,redirect,url_for
from pathlib import Path
from .forms import IniForm
from . import rpi
from ..models import Data, db
from ..utils import parse_resp, BaseResp


@rpi.route('/rpi/', methods=['GET', 'POST'])
def index():
    return render_template('rpi/index.html')


@rpi.route('/rpi/temp/', methods=['GET', 'POST'])
def temp():
    return render_template('rpi/temp.html')


@rpi.route('/rpi/pics/', methods=['GET', 'POST'])
def pics():
    photos_path = Path(current_app.config['BASEDIR'], 'app/static/photos')
    photos = [x.name for x in photos_path.iterdir()]
    photos.sort(reverse=True)
    return render_template('rpi/pics.html', pics=photos)


@rpi.route('/rpi/ping/', methods=['POST', 'GET'])
def ping():
    """提交温湿度数据接口,写入数据库
    methods:POST
    type:json
    {'temp':摄氏度:float,'humidity':湿度:float}
    """
    resp = parse_resp(request)
    print(resp)
    temp = resp.get('temp')
    humidity = resp.get('humidity')
    if (temp and humidity) is None:
        return BaseResp(code=500, msg="参数缺失温湿度").parse_resp()

    try:
        data = Data(temp=temp, humidity=humidity)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        return BaseResp(code=500,
                        msg=f"存数据库失败,请检查数据格式{type(data.temp)} {type(data.humidity)}",
                        data={'why': e}).parse_resp()

    return BaseResp(msg="温湿度上传成功",
                    data=f"温度:{data.temp} 湿度:{data.humidity} 时间:{data.timestamp}").parse_resp()


@rpi.route('/rpi/getdata/', methods=['GET', 'POST'])
def get_data():
    """获取温湿度数据的接口"""
    datas = Data.query.order_by(Data.timestamp).all()
    times = [
        data.to_dict()['time']
        for data in datas
    ]
    temps = [
        data.to_dict()['temp']
        for data in datas
    ]
    humiditys = [
        data.to_dict()['humidity']
        for data in datas
    ]

    return BaseResp(msg="获取全部数据成功！", data={'times': times, 'temps': temps, 'humiditys': humiditys}).parse_resp()


@rpi.route('/rpi/remove_all/', methods=['GET', 'POST'])
def remove_all():
    """清空数据表"""
    db.session.execute('delete from datas;')
    db.session.commit()
    return BaseResp(msg="清空表数据成功!").parse_resp()


@rpi.route('/rpi/upload_photo/', methods=['POST', 'GET'])
def upload_photo():
    """上传图片并保存在 /static/photos 目录
    支持滚动保存
    """
    photos_path = Path(current_app.config['BASEDIR'], 'app/static/photos')
    # 列出目录下的文件
    photos = [str(x) for x in photos_path.iterdir()]
    photos.sort(reverse=True)
    while True:
        if len(photos) >= 6:
            # 当有5张图片时删除最旧的
            rm_file = photos[-1]
            Path(rm_file).unlink()
            photos.remove(rm_file)
            print(f"删除文件{rm_file}成功")
        else:
            break
    if request.method == 'POST':
        img = request.files['image']
        if img:
            img.save(Path(photos_path, img.filename))
            return BaseResp(msg=f"{img.filename}文件上传成功!", data=photos).parse_resp()

    return BaseResp(code=500, msg="文件上传失败,在img字段上传.", data=photos).parse_resp()


@rpi.route('/rpi/frp/', methods=['POST', 'GET'])
def frp():
    """
    在线编辑树莓派 FRPC 配置,使得树莓派会自动获取其配置并更新.
    """
    form = IniForm()
    config_path = Path(current_app.config['BASEDIR'], 'app/static/others/frpc.txt')
    if form.validate_on_submit():
        config_path.touch(exist_ok=True)
        config_path.write_text(form.body.data, encoding="utf-8")
        return redirect(url_for('rpi.frp'))

    return render_template('rpi/editor_frp.html', form=form)


@rpi.route('/rpi/get_frpc/', methods=['POST', 'GET'])
def get_frpc():
    """
    获取 frpc 的接口
    """
    config_path = Path(current_app.config['BASEDIR'], 'app/static/others/frpc.txt')
    if not config_path.is_file():
        with open(str(config_path), "w", encoding='utf-8') as c:
            c.write(current_app.config['FRPC_TEMPLATES'])
    return config_path.read_text(encoding='utf-8')
