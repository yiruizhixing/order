# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify
from common.libs.Helper import ops_render, getCurrentDate, iPagination, getDictField
from application import app, db
from common.models.exam.Kaodian import Kaodian
# from common.models.people.People_cat import PeopleCat
from common.models.people.People import People
from common.models.exam.Exam import Exam
from common.models.exam.Exam import DicStatu
from common.libs.UrlManager import UrlManager
from sqlalchemy import or_
route_exam = Blueprint( 'exam_page',__name__ )


@route_exam.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1  # 当前页号，默认为1
    query = Exam.query

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
    list = query.order_by(Exam.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()  # 使用id字段倒序排  # .all()  为取出所有的数据 然后存到列表list

    # cat_mapping = getDictField(PeopleCat,"id","id",[])
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req  # 搜索框内容
    # resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    # resp_data['cat_mapping'] = cat_mapping
    resp_data['current'] = 'index'
    return ops_render( "exam/index.html", resp_data)

# 考试详情展示页面
@route_exam.route( "/info" )
def info():
    resp_data = {}
    req = request.args  # 参数多时用values ,参数少时用args
    id = int(req.get("id",0))
    reback_url = UrlManager.buildUrl("/exam/index")
    if id < 1:
        return redirect(reback_url)
    info = Exam.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)


    resp_data['info'] = info
    resp_data['current'] = 'index'
    return ops_render( "exam/info.html", resp_data )


# 新增、编辑考试
@route_exam.route( "/set",methods=["GET", "POST"] )
def set():
    if request.method == "GET":
        resp = {'code': 200, 'msg': '操作成功', 'data': ''}
        resp_data = {}
        req = request.args  # 参数多时用values ,参数少时用args
        id = req['id'] if 'id' in req else 0
        info = Exam.query.filter_by(id=id).first()
        if info and info.exam_status !=7:              # 如果考试不是开启状态，则不允许编辑
            return redirect(UrlManager.buildUrl("/exam/index"))

        exam_cat_list = DicStatu.query.filter_by(dic_id = 1).all()
        resp_data['exam_cat_list'] = exam_cat_list
        resp_data['info'] = info
        resp_data['current'] = 'set'
        return ops_render("exam/set.html", resp_data)

    # 下面是POST处理
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                                    # 参数多时用values ,参数少时用args
    id = req['id'] if 'id' in req else 0                    # 获取当前用户id
    exam_cat = req['exam_cat'] if 'exam_cat' in req else ''
    exam_name = req['exam_name'] if 'exam_name' in req else ''

    exam_date = req['exam_date'] if 'exam_date' in req else ''
    summary = req['summary'] if 'summary' in req else ''

    if len(exam_cat) < 1:
        resp['code'] = -1
        resp['msg'] = "请选择考试分类"
        return jsonify(resp)
    if exam_name is None or len(exam_name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的考试名称"
        return jsonify(resp)

    exam_info = Exam.query.filter_by(id=id).first()

    if exam_info:
        model_exam = exam_info
    else:
        model_exam = Exam()
        model_exam.exam_status = 7
        model_exam.created_time = getCurrentDate()

    model_exam.exam_cat = exam_cat
    model_exam.exam_name = exam_name
    model_exam.exam_date = exam_date
    model_exam.summary = summary

    model_exam.updated_time = getCurrentDate()

    # 提交信息
    db.session.add(model_exam)
    db.session.commit()
    return jsonify(resp)


# 考点列表    不用分页
@route_exam.route( "/kaodian" )
def kaodian():
    resp_data = {}
    req = request.values
    query = Kaodian.query

    # 考点有效无效查询
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Kaodian.status == int(req['status']))

    list = query.order_by(  Kaodian.id.asc() ).all()     # 使用正序排  # .all()  为取出所有的数据 然后存到列表list
    resp_data['list'] = list
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'kaodian'
    return ops_render( "exam/kaodian.html", resp_data )


# 考点增加 编辑
@route_exam.route( "/kaodian-set", methods=["GET", "POST"] )
def kaodianSet():
    if request.method == "GET":
        resp_data = {}
        req = request.args                                  # 参数少时用args
        id = int(req.get("id", 0))     # 获取当前id
        info = None
        if id:  # 如果uid存在,说明进入的是编辑页面，否则进入的是新增页面
            info = Kaodian.query.filter_by(id=id).first()  # 前端页面显示当前用户信息
        resp_data['info'] = info  # 把当前登录账户信息返回前端显示
        resp_data['current'] = 'cat'
        return ops_render( "exam/kaodian_set.html", resp_data)

    # 下面是POST处理
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                                    # 参数多时用values ,参数少时用args

    id = req['id'] if 'id' in req else 0                    # 获取当前用户id
    name = req['name'] if 'name' in req else ''
    address = req['address'] if 'address' in req else ''
    tel = req['tel'] if 'tel' in req else ''
    linkman = req['linkman'] if 'linkman' in req else ''
    kaochang = int(req['kaochang']) if ('kaochang' in req and int(req['kaochang']) > 0) else 1

    # 参数有效性判断
    if name is None or len(name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的考点名称"
        return jsonify(resp)

    kaodian_info = Kaodian.query.filter_by(id=id).first()
    if kaodian_info:    # 进入的是编辑功能
        model_kaodian_info = kaodian_info
    else:                # 进入的是新增功能
        model_kaodian_info = Kaodian()
        model_kaodian_info.created_time = getCurrentDate()

    model_kaodian_info.name = name
    model_kaodian_info.address = address
    model_kaodian_info.tel = tel
    model_kaodian_info.linkman = linkman
    model_kaodian_info.kaochang = kaochang
    model_kaodian_info.updated_time = getCurrentDate()

    # 提交信息
    db.session.add( model_kaodian_info )
    db.session.commit()
    return jsonify( resp )


# 删除恢复考点操作
@route_exam.route("/kaodian-ops", methods=["POST"])
def kaodianOps():
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的考点"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
        return jsonify(resp)

    kaodian_info = Kaodian.query.filter_by(id=id).first()
    if not kaodian_info:
        resp['code'] = -1
        resp['msg'] = "指定分类不存在，请重试"
        return jsonify(resp)
    if act == "remove":
        kaodian_info.status = 0
    elif act == "recover":
        kaodian_info.status = 1

    # 提交信息
        kaodian_info.update_time = getCurrentDate()
    db.session.add(kaodian_info)
    db.session.commit()
    return jsonify(resp)


# 删除恢复考试操作
@route_exam.route("/ops", methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的考试"
        return jsonify(resp)
    if act not in [ 'recover', 'pause']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
        return jsonify(resp)

    exam_info = Exam.query.filter_by(id=id).first()
    if not exam_info:
        resp['code'] = -1
        resp['msg'] = "指定考试不存在，请重试"
        return jsonify(resp)
    if act == "pause":
        exam_info.exam_status = 6
    elif act == "recover":
        exam_info.exam_status = 7

    # 提交信息
    exam_info.update_time = getCurrentDate()
    db.session.add(exam_info)
    db.session.commit()
    return jsonify(resp)

