from flask import make_response, Response, request
import json
from pydantic import BaseModel
from typing import Any


class BaseResp(BaseModel):
    """主API响应类"""
    code: int = 200
    msg: Any
    data: Any = []

    def parse_resp(self):
        """生成返回响应"""
        return make_response(
            Response(
                json.dumps(
                    self.dict(), ensure_ascii=False, sort_keys=False
                ),
                mimetype='application/json',
            ),
            self.code
        )


def parse_resp(resp: request) -> dict:
    """解析请求对象并以字典的形式返回"""
    if resp.method == 'POST':
        data = resp.form

    elif resp.method == 'GET':
        data = resp.args

    return dict(data)
