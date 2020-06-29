# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify, g, render_template
from common.libs.Helper import ops_render, getCurrentDate, iPagination, getDictField
from application import app, db
from common.models.news.News import News
from common.libs.UrlManager import UrlManager
from decimal import Decimal
from sqlalchemy import or_
route_news = Blueprint( 'news_page',__name__ )

# 通知首页
@route_news.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1  # 当前页号，默认为1
    query = News.query

    # 用户搜索处理
    if 'mix_kw' in req:
        rule = or_(News.name.ilike("%{0}%".format(req['mix_kw'])),
                   News.tags.ilike("%{0}%".format(req['mix_kw'])))  # 需要导入 sqlalchemy import or_   or 查询
        # ilike 不区分大小写 对用户名或手机号查询 or为混合查询
        query = query.filter(rule)
    # 用户账号有效无效查询
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(News.status == int(req['status']))

    if 'cat_id' in req and int(req['cat_id']) > 0:
        query = query.filter(News.cat_id == int(req['cat_id']))

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
    list = query.order_by(News.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()  # 使用uid字段倒序排  # .all()  为取出所有的数据 然后存到列表list

    # cat_mapping = getDictField(FoodCat,"id","id",[])
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req  # 搜索框内容
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    # resp_data['cat_mapping'] = cat_mapping
    resp_data['current'] = 'index'
    return ops_render( "news/index.html", resp_data)

# 通知内容详情展示页面
@route_news.route( "/info" )
def info():
    resp_data = {}
    req = request.args  # 参数多时用values ,参数少时用args
    id = int(req.get("id",0))
    reback_url = UrlManager.buildUrl("/news/index")
    if id < 1:
        return redirect(reback_url)
    info = News.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

    # stock_change_list = FoodStockChangeLog.query.filter(FoodStockChangeLog.food_id == id).order_by(FoodStockChangeLog.id.desc()).all()
    resp_data['info'] = info
    # resp_data['stock_change_list'] = stock_change_list
    resp_data['current'] = 'index'
    return ops_render( "news/info.html", resp_data )


# 通知详情编辑
@route_news.route( "/set",methods=["GET", "POST"] )
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args  # 参数多时用values ,参数少时用args
        id = req['id'] if 'id' in req else 0
        info = News.query.filter_by(id=id).first()
        if info and info.status !=1:
            return redirect(UrlManager.buildUrl("/news/index"))

        resp_data['info'] = info
        resp_data['current'] = 'index'
        return ops_render("news/set.html", resp_data)

    # 下面是POST处理
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                                    # 参数多时用values ,参数少时用args
    id = req['id'] if 'id' in req else 0                    # 获取当前用户id
    name = req['name'] if 'name' in req else ''
    summary = req['summary'] if 'summary' in req else ''
    tags = req['tags'] if 'tags' in req else ''

    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的名称"
        return jsonify(resp)
    if summary is None or len(summary) < 3:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的内容描述"
        return jsonify(resp)
    food_info = News.query.filter_by(id=id).first()
    if food_info:
        model_food = food_info
    else:
        model_food = News()
        model_food.status = 1
        model_food.created_time = getCurrentDate()

    model_food.name = name
    model_food.summary = summary
    model_food.tags = tags
    model_food.updated_time = getCurrentDate()
    db.session.add(model_food)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()

    return jsonify(resp)

# 删除恢复通知操作
@route_news.route("/ops", methods=["POST"])
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

    food_info = News.query.filter_by(id=id).first()
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

