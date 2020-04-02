# -*- coding: utf-8 -*-
from flask import Blueprint, flash, request, jsonify, redirect, session
from common.libs.Helper import ops_render, getCurrentDate
from common.models.exam.Exam import Exam
from common.models.exam.Exam_kemu import ExamKemu
from common.models.exam.Kaodian import Kaodian
from common.models.exam.Exam_kaodian import ExamKaodian
from application import db, app
import json
from common.libs.UrlManager import UrlManager


route_examset = Blueprint('examset_page', __name__)

# 基本设置 首页显示 基本设置保存
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


# 考点设置
@route_examset.route( "/kaodian", methods=["GET", "POST"] )
def kaodian():
    examid = int(session.get("examid"))  # 当前考试id
    exam_kaodian_list = ExamKaodian.query.filter_by(exam_id=examid)   # 查出已经安排的考点表  有了.all() 返回的就是列表
    exam_kaodian_list_temp = exam_kaodian_list.all()                  # 有了.all() 返回的就是列表
    old_temp = []
    for temp in exam_kaodian_list_temp:
        old_temp.append(temp.kaodian_id)                                # 列表 临时存放原有已选 考点id

    if request.method == "GET":
        resp_data = {}
        query = Kaodian.query                                    # 查出全部考点
        query = query.filter(Kaodian.status == 1)                # 考点有效无效查询
        kaodian_list = query.order_by(Kaodian.id.asc()).all()    # 使用正序排  # .all()  为取出所有的数据 然后存到列表kaodian_list
        kaodian_list_temp = []
        for temp in kaodian_list:                                # 如果考点没有在已选考点表中，则加入备选表中
            if temp.id not in old_temp:
                kaodian_list_temp.append(temp)
        resp_data['list'] = kaodian_list_temp                    # 备用考点列表
        resp_data['exam_kaodian_list'] = exam_kaodian_list       # 已选考点列表
        resp_data['current'] = 'kaodian'
        return ops_render( "examset/kaodian.html", resp_data )
    # post
    exam_name = session.get("exam_name")  # 当前考试name
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                              # 参数多时用values ,参数少时用args
    # 将JSON数据解码为dict（字典）
    new_kaodiandata = json.loads(req['data'])
    new_temp = []                                     # 列表 临时存放新选 考点id
    for temp in new_kaodiandata:                      # 添加每条记录
        new_temp.append(int(temp['kaodianid']))
        # 查出考点安排表中原有的安排
        exam_kaodian_have = exam_kaodian_list.filter(ExamKaodian.kaodian_id == int(temp['kaodianid'])).first()
        if not exam_kaodian_have:                     # 若原有的安排表中没有，则填加  ----新增考点
            exam_kaodian_info = ExamKaodian()
            exam_kaodian_info.exam_id = examid
            exam_kaodian_info.exam_name = exam_name
            exam_kaodian_info.kaodian_id = int(temp['kaodianid'])
            exam_kaodian_info.kaodian_name = temp['kaodianname']
            exam_kaodian_info.created_time = getCurrentDate()
            exam_kaodian_info.updated_time = getCurrentDate()
            db.session.add(exam_kaodian_info)

    # 若原有的安排表中有，新安排表中无，则删除  ----删除考点
    for tempi in old_temp:
        if tempi not in new_temp:
            exam_kaodian_del_info = ExamKaodian.query.filter(ExamKaodian.exam_id == examid, ExamKaodian.kaodian_id == tempi).first()
            db.session.delete(exam_kaodian_del_info)
    # 提交信息
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()
    return jsonify(resp)



@route_examset.route( "/kaochang" )
def kaochang():
    return ops_render( "examset/kaochang.html" )


