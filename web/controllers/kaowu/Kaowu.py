# -*- coding: utf-8 -*-
from application import app, db
from flask import Blueprint, request, redirect, jsonify, g, session
from common.libs.Helper import ops_render, getCurrentDate
from common.models.exam.Exam_kaowu import ExamKaowu
from common.models.people.People_cat import PeopleCat
from common.models.people.People import People
from common.models.exam.Exam_kaodian import ExamKaodian
from common.models.exam.Exam import Exam
from sqlalchemy import or_, and_

route_kaowu = Blueprint( 'kaowu_page', __name__ )

@route_kaowu.route( "/index" )
def index():
    return ops_render( "kaowu/index.html" )


# 考区人员安排
@route_kaowu.route( "/kqarrange", methods=["GET", "POST"] )
def kqarrange():
    exam_id = int(session.get("examid"))  # 当前考试id         # 考试id
    if request.method == "GET":
        resp_data = {}
        req = request.args                                 # 参数多时用values ,参数少时用args

        # 填加人员查找处理  此为select2的api接口，也为考点人员设置使用
        if 'search' in req:
            query = People.query.filter(People.status == 1)                   # 查找正常状态的人员
            rule = or_(People.name.ilike("%{0}%".format(req['search'])),
                       People.nickname.ilike("%{0}%".format(req['search'])))  # 需要导入 sqlalchemy import or_   or 查询
                                                                # ilike 不区分大小写 对用户名或手机号查询 or为混合查询
            query = query.filter(rule).all()   # 返回所有查询记录的 列表
            data = []                          # 取出query列表中的有用信息，转到data列表中
            for ele in query:
                dic1 = {'id': ele.id, 'text': ele.name}
                data.append(dic1)
            # data1 = [{'id': 1, 'text': '张三'}, {'id': 2, 'text': 'lisi'}, {'id': 3, 'text': '王五'}]  # 测试数据
            return jsonify(data)

        # 查询考务安排表中的考区人员
        kaoqu_people_list = ExamKaowu.query.filter(ExamKaowu.exam_id == exam_id, ExamKaowu.workplace == "考区") .all()
        cat_list = PeopleCat.query.all()                      # 查询岗位分类
        resp_data['kaoqu_people_list'] = kaoqu_people_list
        resp_data['cat_list'] = cat_list
        resp_data['current'] = 'kqarrange'
        return ops_render("kaowu/kqarrange.html", resp_data)

    # 下面是POST处理
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                                       # 参数多时用values ,参数少时用args
    name_id = req['name_id'] if 'name_id' in req else 0        # 当前姓名id
    job_id = req['job_id'] if 'job_id' in req else 0           # 岗位id
    job = req['job'] if 'job' in req else ''                   # 工作岗位
    name = req['name'] if 'name' in req else ''                # 姓名
    beizhu1 = req['beizhu1'] if 'beizhu1' in req else ''       # 所填备注
    exam = Exam.query.filter_by(id=exam_id).first()
    workdays = exam.days  # 工作天数
    canbu = exam.canbu  # 餐补天数

    model_kaowu = ExamKaowu()
    model_kaowu.exam_id = exam_id
    model_kaowu.job = job
    model_kaowu.job_id = job_id
    model_kaowu.beizhu1 = beizhu1
    model_kaowu.beizhu2 = name
    model_kaowu.workdays = workdays        # 工作天数
    model_kaowu.canbu = canbu              # 餐补天数
    model_kaowu.workplace = "考区"
    name_id = int(name_id)
    model_kaowu.name_id = name_id          # 人员id
    model_kaowu.created_time = getCurrentDate()
    model_kaowu.updated_time = getCurrentDate()
    # 提交信息
    db.session.add(model_kaowu)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()
    return jsonify(resp)


# 删除考区人员 以及考点安排中的 其他人员安排
@route_kaowu.route("/kq-ops", methods=["POST"])
def kqOps():
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要删除的人员"
        return jsonify(resp)
    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
        return jsonify(resp)

    model_kaowu_info = ExamKaowu.query.filter_by(id=id).first()
    if not model_kaowu_info:
        resp['code'] = -1
        resp['msg'] = "指定人员安排不存在，请重试"
        return jsonify(resp)
    if act == "remove":
        db.session.delete(model_kaowu_info)  # 使用 db.session.delete() 方法删除记录，传入模型实例
        db.session.commit()
    return jsonify(resp)


# 考点人员安排
@route_kaowu.route( "/kdarrange", methods=["GET", "POST"] )
def kdarrange():
    examid = int(session.get("examid"))  # 当前考试id
    # exam_name = session.get("exam_name")  # 当前考试name

    if request.method == "GET":
        # resp = {'code': 200, 'msg': '操作成功', 'data': ''}
        # req = request.values  # 参数多时用values ,参数少时用args
        resp_data = {}
        kaodian_list = ExamKaodian.query.filter_by(exam_id=examid).all()
        # 查询考务安排表中的考区人员
        kaodian_people_list = ExamKaowu.query.filter(ExamKaowu.exam_id == examid, ExamKaowu.workplace == "考点").all()
        cat_list = PeopleCat.query.all()                      # 查询岗位分类
        # 查询出其他人员安排
        up_list = [6, 7, 8, 9, 10, 11, 18, 19]  # job_id 巡视组长 	副巡视组长 	试卷押运 	流动巡视 	巡视人员 	反作弊小组 	治安门检 	司机
        other_list = []  # 取出kaodian_people_list列表中的其他人员信息，转到data列表中
        for ele in kaodian_people_list:
            if ele.job_id not in up_list:
                dic1 = {'id': ele.id, 'job': ele.job, 'name': ele.name.name, 'beizhu': ele.beizhu1, 'kaodian': ele.kaodian}
                other_list.append(dic1)

        resp_data['other_list'] = other_list
        resp_data['cat_list'] = cat_list
        resp_data['kaodian_people_list'] = kaodian_people_list
        resp_data['kaodian_list'] = kaodian_list
        resp_data['current'] = 'kdarrange'
        return ops_render("kaowu/kdarrange.html", resp_data)

    # POST 增加人员安排 入数据库
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values  # 参数多时用values ,参数少时用args
    name_id = req['name_id'] if 'name_id' in req else 0      # 当前姓名id
    beizhu2 = req['name'] if 'name' in req else ''           # 姓名
    job = req['job'] if 'job' in req else ''                 # 工作岗位
    job_id = req['job_id'] if 'job_id' in req else ''        # 工作岗位
    kaodian = req['kaodian'] if 'kaodian' in req else ''     # 考点名称
    kdid = req['kdid'] if 'kdid' in req else 0               # 考点id
    beizhu1 = req['beizhu1'] if 'beizhu1' in req else ''     # 备注
    exam = Exam.query.filter_by(id=examid).first()
    workdays = exam.days         # 工作天数
    canbu = exam.canbu           # 餐补天数

    model_kaowu = ExamKaowu()
    model_kaowu.exam_id = examid
    model_kaowu.job = job
    model_kaowu.job_id = int(job_id)
    model_kaowu.kaodian = kaodian          # 考点名称
    model_kaowu.beizhu2 = beizhu2          # 姓名
    model_kaowu.beizhu1 = beizhu1          # 备注
    model_kaowu.workdays = workdays        # 工作天数
    model_kaowu.canbu = canbu              # 餐补天数
    model_kaowu.workplace = "考点"
    model_kaowu.name_id = int(name_id)          # 人员id
    model_kaowu.created_time = getCurrentDate()
    model_kaowu.updated_time = getCurrentDate()

    # 提交信息
    db.session.add(model_kaowu)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()
    return jsonify(resp)


# 删除考点人员
@route_kaowu.route("/kd-ops", methods=["POST"])
def kdOps():
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values
    examid = int(session.get("examid"))  # 当前考试id
    job_id = req['job_id'] if 'job_id' in req else 0
    # name = req['name'] if 'name' in req else ''
    name_id = req['name_id'] if 'name_id' in req else ''
    kaodian = req['kaodian'] if 'kaodian' in req else ''
    if not name_id:
        resp['code'] = -1
        resp['msg'] = "要删除的人员安排不存在"
        return jsonify(resp)

    model_kaowu_info = ExamKaowu.query.filter(ExamKaowu.exam_id == examid, ExamKaowu.workplace == "考点")
    model_kaowu_info = model_kaowu_info.filter(ExamKaowu.kaodian == kaodian)
    model_kaowu_info = model_kaowu_info.filter(ExamKaowu.job_id == job_id)
    model_kaowu_info = model_kaowu_info.filter(ExamKaowu.name_id == name_id).first()
    if not model_kaowu_info:
        resp['code'] = -1
        resp['msg'] = "指定人员安排不存在，请重试"
        return jsonify(resp)
    # 提交信息
    db.session.delete(model_kaowu_info)  # 使用 db.session.delete() 方法删除记录，传入模型实例
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()
    return jsonify(resp)


# 可询已安排考点人员，返回
# @route_kaowu.route( "/kqarrange/slectedjson" )
# def selectedjson():
#     query = People.query.filter(People.status == 1)  # 查找正常状态的人员
#     data = []  # 取出query列表中的有用信息，转到data列表中
#     for ele in query:
#         dic1 = {'id': ele.id, 'text': ele.name}
#         data.append(dic1)
#     data1 = [{'id': 1, 'text': '张三222'}, {'id': 2, 'text': 'lisi'}, {'id': 3, 'text': '王五'}]    # 测试数据
#     data2 = [{'id': 1, 'text': '张三'}]  # 测试数据
#     return jsonify(data1)


