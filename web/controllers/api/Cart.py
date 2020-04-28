# -*- coding: utf-8 -*-
# 接受小程序购物车操作
from web.controllers.api import route_api
from flask import request, jsonify, g
from common.models.food.Food import Food

# 加入购物车操作
@route_api.route("/cart/set", methods = ["POST"])
def setCart():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    number = int(req['number']) if 'number' in req else 0
    food_id = int(req['id']) if 'id' in req else 0
    if food_id < 1 or number < 1:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-1"
        return jsonify(resp)

    member_info = g.member_info
    if not member_info:     # 如果用户信息不存在
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-2"
        return jsonify(resp)
    food_info = Food.query.filter_by(id=food_id).first()
    if not food_info:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-3"
        return jsonify(resp)
    if food_info.stock < number:
        resp['code'] = -1
        resp['msg'] = "添加购物车失败-库存不足"
        return jsonify(resp)

    return jsonify(resp)
