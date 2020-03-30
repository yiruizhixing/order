# -*- coding: utf-8 -*-
from flask import Blueprint, flash, request, jsonify, redirect, session
from common.libs.Helper import ops_render, getCurrentDate
from common.models.exam.Exam import Exam
from common.models.exam.Exam_kemu import ExamKemu
from application import db
import json
from common.libs.UrlManager import UrlManager



route_examset = Blueprint('examset_page', __name__)


@route_examset.route( "/index", methods=["GET", "POST"] )
def index():
    if request.method == "GET":
        resp_data = {}
        req = request.args               # 参数多时用values ,参数少时用args
        id = int(session.get("examid"))
        # reback_url = UrlManager.buildUrl("/examset/index")
        # flash("考试id" + str(id))
        if id < 1:
            pass  # return redirect(reback_url)
            flash("考试不正确，请选择")
        info = Exam.query.filter_by(id=id).first()
        kemu_info = ExamKemu.query.filter_by(exam_id=id).all()
        if not info:
           pass    # return redirect(reback_url)
        resp_data['info'] = info
        resp_data['kemu_info'] = kemu_info
        resp_data['current'] = 'index'
        return ops_render("examset/index.html", resp_data)


    # post
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values  # 参数多时用values ,参数少时用args
    id = req['id'] if 'id' in req else 0  # 获取当前用户id
    keshu = req['keshu'] if 'keshu' in req else ''
    canbu = req['canbu'] if 'canbu' in req else ''
    days = req['days'] if 'days' in req else ''

    exam_info = Exam.query.filter_by(id=id).first()
    if exam_info:
        model_exam = exam_info
    else:
        resp['code'] = -1
        resp['msg'] = "请选择考试"
        return jsonify(resp)

    model_exam.keshu = int(keshu)
    model_exam.canbu = int(canbu)
    model_exam.days = float(days)
    model_exam.updated_time = getCurrentDate()

    # 提交信息
    try:
        db.session.add(model_exam)
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()

    return jsonify(resp)


# 科目设置保存
@route_examset.route( "/kemusave", methods=["POST"] )
def kemusave():
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                                     # 参数多时用values ,参数少时用args
    # 将JSON数据解码为dict（字典）
    kemudata = json.loads(req['data'])
    examid = int(session.get("examid"))                      # 当前考试id
    exam_name = session.get("exam_name")
    for temp in kemudata:                                    # 添加每条记录
        if int(temp['kemuid']) == 0:    # 若kemuid为0，则新建实例
            exam_kemu_info = ExamKemu()
            exam_kemu_info.created_time = getCurrentDate()
        else:                           # 若kemuid不为0，则为修改，查询实例
            exam_kemu_info = ExamKemu.query.filter_by(id=temp['kemuid']).first()

        exam_kemu_info.updated_time = getCurrentDate()
        exam_kemu_info.exam_id = examid
        exam_kemu_info.exam_name = exam_name
        exam_kemu_info.changci = temp['changci']
        exam_kemu_info.kemu_name = temp['kemuName']
        exam_kemu_info.start_time = temp['startTime'] if temp['startTime'] != "" else exam_kemu_info.updated_time
        exam_kemu_info.last_time = temp['lastTime'] if temp['lastTime'] != "" else 120
        exam_kemu_info.kaochang = int(temp['kaochang']) if temp['kaochang'] != "" else 1

        db.session.add(exam_kemu_info)
    # 提交信息
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()
    return jsonify(resp)


# 科目设置删除
@route_examset.route( "/kemudel", methods=["POST"] )
def kemudel():
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values  # 参数多时用values ,参数少时用args
    # 将JSON数据解码为dict（字典）
    kemudata = json.loads(req['data'])
    examid = int(session.get("examid"))  # 当前考试id
    exam_name = session.get("exam_name")
    for temp in kemudata:
        if int(temp['kemuid']) != 0:
            exam_kemu_info = ExamKemu.query.filter_by(id=temp['kemuid']).first()
            if not exam_kemu_info:
                resp['code'] = -1
                resp['msg'] = "指定信息不存在，请重试"
                return jsonify(resp)
            db.session.delete(exam_kemu_info)  # 使用 db.session.delete() 方法删除记录，传入模型实例

    # 提交信息
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()
    return jsonify(resp)


@route_examset.route( "/kaodian" )
def kaodian():
    return ops_render( "examset/kaodian.html" )



@route_examset.route( "/kaochang" )
def kaochang():
    return ops_render( "examset/kaochang.html" )


