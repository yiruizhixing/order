# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify
from common.libs.Helper import ops_render, getCurrentDate, iPagination, getDictField
from application import app, db
from common.models.food.FoodCat import FoodCat
from common.models.people.People_cat import PeopleCat
from common.models.food.Food import Food
from common.models.people.People import People
from common.models.food.foodStockChangeLog import FoodStockChangeLog
from common.libs.UrlManager import UrlManager
from decimal import Decimal
from sqlalchemy import or_
route_people = Blueprint( 'people_page',__name__ )


@route_people.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1  # 当前页号，默认为1
    query = People.query

    # 用户搜索处理
    if 'mix_kw' in req:
        rule = or_(People.name.ilike("%{0}%".format(req['mix_kw'])),
                   People.nickname.ilike("%{0}%".format(req['mix_kw'])))  # 需要导入 sqlalchemy import or_   or 查询
        # ilike 不区分大小写 对用户名或手机号查询 or为混合查询
        query = query.filter(rule)
    # 用户账号有效无效查询
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(People.status == int(req['status']))

    if 'cat_id' in req and int(req['cat_id']) > 0:
        query = query.filter(People.cat_id == int(req['cat_id']))

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
    list = query.order_by(People.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()  # 使用uid字段倒序排  # .all()  为取出所有的数据 然后存到列表list

    cat_mapping = getDictField(PeopleCat,"id","id",[])
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req  # 搜索框内容
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['cat_mapping'] = cat_mapping
    resp_data['current'] = 'index'
    return ops_render( "people/index.html", resp_data)

# 人员详情展示页面
@route_people.route( "/info" )
def info():
    resp_data = {}
    req = request.args  # 参数多时用values ,参数少时用args
    id = int(req.get("id",0))
    reback_url = UrlManager.buildUrl("/people/index")
    if id < 1:
        return redirect(reback_url)
    info = People.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)


    resp_data['info'] = info
    resp_data['current'] = 'index'
    return ops_render( "people/info.html", resp_data )


# 人员详情编辑
@route_people.route( "/set",methods=["GET", "POST"] )
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args  # 参数多时用values ,参数少时用args
        id = req['id'] if 'id' in req else 0
        info = People.query.filter_by(id=id).first()
        if info and info.status !=1:
            return redirect(UrlManager.buildUrl("/people/index"))

        cat_list = PeopleCat.query.all()
        resp_data['info'] = info
        resp_data['cat_list'] = cat_list
        resp_data['current'] = 'index'
        return ops_render("people/set.html", resp_data)

    # 下面是POST处理
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                                    # 参数多时用values ,参数少时用args
    id = req['id'] if 'id' in req else 0                    # 获取当前用户id
    cat_id = req['cat_id'] if 'cat_id' in req else ''
    name = req['name'] if 'name' in req else ''

    xunkao_id = req['xunkao_id'] if 'xunkao_id' in req else ''
    danwei = req['danwei'] if 'danwei' in req else ''
    bumen = req['bumen'] if 'bumen' in req else ''
    weight = req['weight'] if 'weight' in req else ''
    chepai = req['chepai'] if 'chepai' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    sfzh = req['sfzh'] if 'sfzh' in req else ''
    bankcard = req['bankcard'] if 'bankcard' in req else ''
    bankaddr = req['bankaddr'] if 'bankaddr' in req else ''
    address = req['address'] if 'address' in req else ''

    if len(cat_id) < 1:
        resp['code'] = -1
        resp['msg'] = "请选择分类"
        return jsonify(resp)
    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名"
        return jsonify(resp)

    people_info = People.query.filter_by(id=id).first()

    if people_info:
        model_people = people_info
    else:
        model_people = People()
        model_people.status = 1
        model_people.created_time = getCurrentDate()

    model_people.cat_id = cat_id
    model_people.name = name
    model_people.xunkao_id = xunkao_id
    model_people.danwei = danwei
    model_people.bumen = bumen
    model_people.weight = weight
    model_people.sfzh = sfzh
    model_people.chepai = chepai
    model_people.mobile = mobile
    model_people.bankcard = bankcard
    model_people.bankaddr = bankaddr
    model_people.address = address

    model_people.updated_time = getCurrentDate()

    # 提交信息
    db.session.add(model_people)
    db.session.commit()
    return jsonify(resp)


# 分类列表    不用分页
@route_people.route( "/cat" )
def cat():
    resp_data = {}
    req = request.values
    query = PeopleCat.query

    # 分类项目有效无效查询
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(PeopleCat.status == int(req['status']))

    list = query.order_by( PeopleCat.weight.desc(), PeopleCat.id.desc() ).all()     # 使用权重、id倒序排  # .all()  为取出所有的数据 然后存到列表list
    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'cat'
    return ops_render( "people/cat.html", resp_data )


# 分类设置
@route_people.route( "/cat-set", methods=["GET", "POST"] )
def catSet():
    if request.method == "GET":
        resp_data = {}
        req = request.args                                  # 参数少时用args
        id = int(req.get("id", 0))     # 获取当前id
        info = None
        if id:  # 如果uid存在,说明进入的是编辑页面，否则进入的是新增页面
            info = PeopleCat.query.filter_by(id=id).first()  # 前端页面显示当前用户信息
        resp_data['info'] = info  # 把当前登录账户信息返回前端显示
        resp_data['current'] = 'cat'
        return ops_render( "people/cat_set.html", resp_data)

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

    people_cat_info = PeopleCat.query.filter_by(id=id).first()
    if people_cat_info:    # 进入的是编辑功能
        model_people_cat = people_cat_info
    else:                # 进入的是新增功能
        model_people_cat = PeopleCat()
        model_people_cat.created_time = getCurrentDate()

    model_people_cat.name = name
    model_people_cat.weight = weight
    model_people_cat.updated_time = getCurrentDate()

    # 提交信息
    db.session.add( model_people_cat )
    db.session.commit()
    return jsonify( resp )


# 删除恢复岗位分类操作
@route_people.route("/cat-ops", methods=["POST"])
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

    people_cat_info = PeopleCat.query.filter_by(id=id).first()
    if not people_cat_info:
        resp['code'] = -1
        resp['msg'] = "指定分类不存在，请重试"
        return jsonify(resp)
    if act == "remove":
        people_cat_info.status = 0
    elif act == "recover":
        people_cat_info.status = 1

    # 提交信息
        people_cat_info.update_time = getCurrentDate()
    db.session.add(people_cat_info)
    db.session.commit()
    return jsonify(resp)


# 删除恢复人员操作
@route_people.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的菜品"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
        return jsonify(resp)

    people_info = People.query.filter_by(id=id).first()
    if not people_info:
        resp['code'] = -1
        resp['msg'] = "指定人员不存在，请重试"
        return jsonify(resp)
    if act == "remove":
        people_info.status = 0
    elif act == "recover":
        people_info.status = 1

    # 提交信息
    people_info.update_time = getCurrentDate()
    db.session.add(people_info)
    db.session.commit()
    return jsonify(resp)

