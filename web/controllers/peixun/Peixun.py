# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify, g, render_template
from common.libs.Helper import ops_render, getCurrentDate, iPagination, getDictField
from application import app, db
from common.models.food.FoodCat import FoodCat
from common.models.food.Food import Food
from common.models.food.foodStockChangeLog import FoodStockChangeLog
from common.libs.UrlManager import UrlManager
from decimal import Decimal
from sqlalchemy import or_
route_peixun = Blueprint( 'peixun_page',__name__ )


@route_peixun.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1  # 当前页号，默认为1
    query = Food.query

    # 用户搜索处理
    if 'mix_kw' in req:
        rule = or_(Food.name.ilike("%{0}%".format(req['mix_kw'])),
                   Food.tags.ilike("%{0}%".format(req['mix_kw'])))  # 需要导入 sqlalchemy import or_   or 查询
        # ilike 不区分大小写 对用户名或手机号查询 or为混合查询
        query = query.filter(rule)
    # 用户账号有效无效查询
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Food.status == int(req['status']))

    if 'cat_id' in req and int(req['cat_id']) > 0:
        query = query.filter(Food.cat_id == int(req['cat_id']))

    # 分页参数
    page_params = {
        'total': query.count(),  # 统计账号总数
        'page_size': app.config['PAGE_SIZE'],  # 每页显示账号数
        'page': page,
        'display': app.config['PAGE_DISPLAY'],  # 展示总页数
        'url': request.full_path.replace("&p={}".format(page), "")
    }
    pages = iPagination(page_params)  # 分页操作
    offset = (page - 1) * app.config['PAGE_SIZE']  # 偏移量，第二页从50开始，第三页从101开始
    list = query.order_by(Food.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()  # 使用uid字段倒序排  # .all()  为取出所有的数据 然后存到列表list

    cat_mapping = getDictField(FoodCat,"id","id",[])
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req     # 搜索框内容
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['cat_mapping'] = cat_mapping
    resp_data['current'] = 'index'
    return ops_render( "peixun/index.html", resp_data)

# 详情展示页面
@route_peixun.route( "/info" )
def info():
    resp_data = {}
    req = request.args  # 参数多时用values ,参数少时用args
    id = int(req.get("id",0))
    reback_url = UrlManager.buildUrl("/peixun/index")
    if id < 1:
        return redirect(reback_url)
    info = Food.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

    stock_change_list = FoodStockChangeLog.query.filter(FoodStockChangeLog.food_id == id).order_by(FoodStockChangeLog.id.desc()).all()
    resp_data['info'] = info
    resp_data['stock_change_list'] = stock_change_list
    resp_data['current'] = 'index'
    return ops_render( "peixun/info.html", resp_data )


# 通知详情编辑
@route_peixun.route( "/set",methods=["GET", "POST"] )
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args  # 参数多时用values ,参数少时用args
        id = req['id'] if 'id' in req else 0
        info = Food.query.filter_by(id=id).first()
        if info and info.status !=1:
            return redirect(UrlManager.buildUrl("/food/index"))

        cat_list = FoodCat.query.filter_by(status=1).all()
        resp_data['info'] = info
        resp_data['cat_list'] = cat_list
        resp_data['current'] = 'index'
        return ops_render("peixun/set.html", resp_data)

    # 下面是POST处理
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                                    # 参数多时用values ,参数少时用args
    id = req['id'] if 'id' in req else 0                    # 获取当前用户id
    cat_id = req['cat_id'] if 'cat_id' in req else ''
    name = req['name'] if 'name' in req else ''
    # price = req['price'] if 'price' in req else ''
    main_image = req['main_image'] if 'main_image' in req else ''
    summary = req['summary'] if 'summary' in req else ''
    # stock = req['stock'] if 'stock' in req else ''
    tags = req['tags'] if 'tags' in req else ''

    # price = Decimal(price).quantize(Decimal('0.00'))    # 转换价格格式

    if len(cat_id) < 1:
        resp['code'] = -1
        resp['msg'] = "请选择分类"
        return jsonify(resp)
    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的名称"
        return jsonify(resp)

    if summary is None or len(summary) < 3:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的描述"
        return jsonify(resp)


    food_info = Food.query.filter_by(id=id).first()
    before_stock = 0
    if food_info:
        model_food = food_info
        before_stock = model_food.stock
    else:
        model_food = Food()
        model_food.status = 1
        model_food.created_time = getCurrentDate()

    model_food.cat_id = cat_id
    model_food.name = name
    # model_food.price = price
    model_food.main_image = main_image
    model_food.summary = summary
    # model_food.stock = stock
    model_food.tags = tags
    model_food.updated_time = getCurrentDate()

    db.session.add(model_food)
    ret = db.session.commit()

    # 处理库存变化
    # model_stock_change = FoodStockChangeLog()
    # model_stock_change.food_id = model_food.id
    # model_stock_change.unit = int(stock)-int(before_stock)
    # model_stock_change.total_stock = stock
    # model_stock_change.note = ''
    # model_stock_change.created_time = getCurrentDate()
    # db.session.add(model_stock_change)
    # db.session.commit()
    return jsonify(resp)


# 分类列表    不用分页
@route_peixun.route( "/cat" )
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
    return ops_render( "peixun/cat.html", resp_data )


# 分类设置
@route_peixun.route( "/cat-set", methods=["GET", "POST"] )
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
        return ops_render( "peixun/cat_set.html", resp_data)

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


# 删除恢复分类操作
@route_peixun.route("/cat-ops", methods=["POST"])
def catOps():
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


# 删除恢复通知操作
@route_peixun.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的通知"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
        return jsonify(resp)

    food_info = Food.query.filter_by(id=id).first()
    if not food_info:
        resp['code'] = -1
        resp['msg'] = "指定通知不存在，请重试"
        return jsonify(resp)
    if act == "remove":
        food_info.status = 0
    elif act == "recover":
        food_info.status = 1

    # 提交信息
    food_info.update_time = getCurrentDate()
    db.session.add(food_info)
    db.session.commit()
    return jsonify(resp)


