# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify, g, render_template
from common.libs.Helper import ops_render, getCurrentDate
from application import app, db
from common.models.food.FoodCat import FoodCat
route_food = Blueprint( 'food_page',__name__ )


@route_food.route( "/index" )
def index():
    return ops_render( "food/index.html" )

@route_food.route( "/info" )
def info():
    return ops_render( "food/info.html" )


@route_food.route( "/set" )
def set():
    return ops_render( "food/set.html" )


# 分类列表    不用分页
@route_food.route( "/cat" )
def cat():
    resp_data = {}
    req = request.values
    query = FoodCat.query

    # 分类项目有效无效查询
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(FoodCat.status == int(req['status']))

    list = query.order_by( FoodCat.weight.desc(), FoodCat.id.desc() ).all()     # 使用权重、id倒序排  # .all()  为取出所有的数据 然后存到列表list
    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'cat'
    return ops_render( "food/cat.html", resp_data )


# 菜品分类设置
@route_food.route( "/cat-set", methods=["GET", "POST"] )
def catSet():
    if request.method == "GET":
        resp_data = {}
        req = request.args                                  # 参数少时用args
        id = int(req.get("id", 0))     # 获取当前id
        info = None
        if id:  # 如果uid存在,说明进入的是编辑页面，否则进入的是新增页面
            info = FoodCat.query.filter_by(id=id).first()  # 前端页面显示当前用户信息
        resp_data['info'] = info  # 把当前登录账户信息返回前端显示
        resp_data['current'] = 'cat'
        return ops_render( "food/cat_set.html", resp_data)

    # 下面是POST处理
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                                    # 参数多时用values ,参数少时用args

    id = req['id'] if 'id' in req else 0                    # 获取当前用户id
    name = req['name'] if 'name' in req else ''
    weight = int(req['weight']) if ('weight' in req and int(req['weight']) > 0) else 1

    # 参数有效性判断
    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的分类名称"
        return jsonify(resp)

    food_cat_info = FoodCat.query.filter_by(id=id).first()
    if food_cat_info:    # 进入的是编辑功能
        model_food_cat = food_cat_info
    else:                # 进入的是新增功能
        model_food_cat = FoodCat()
        model_food_cat.created_time = getCurrentDate()

    model_food_cat.name = name
    model_food_cat.weight = weight
    model_food_cat.updated_time = getCurrentDate()

    # 提交信息
    db.session.add( model_food_cat )
    db.session.commit()
    return jsonify( resp )


# 删除恢复菜品分类操作
@route_food.route("/cat-ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
        return jsonify(resp)

    food_cat_info = FoodCat.query.filter_by(id=id).first()
    if not food_cat_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在，请重试"
        return jsonify(resp)
    if act == "remove":
        food_cat_info.status = 0
    elif act == "recover":
        food_cat_info.status = 1

    # 提交信息
    food_cat_info.update_time = getCurrentDate()
    db.session.add(food_cat_info)
    db.session.commit()
    return jsonify(resp)




