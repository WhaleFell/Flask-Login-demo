from flask import render_template, request, make_response
from . import info
from ..models import Data, db
from ..utils import parse_resp, BaseResp


@info.route('/info/', methods=['GET', 'POST'])
def index():
    return render_template('info/index.html')


@info.route('/ping/', methods=['POST', 'GET'])
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


@info.route('/getdata/', methods=['GET', 'POST'])
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


@info.route('/remove_all/', methods=['GET', 'POST'])
def remove_all():
    """清空数据表"""
    db.session.execute('delete from datas;')
    db.session.commit()
    return BaseResp(msg="清空表数据成功!").parse_resp()
