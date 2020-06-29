# -*- coding: utf-8 -*-
from flask import Blueprint,request, jsonify, session
from common.libs.Helper import ops_render, getCurrentDate
from common.models.bm.BmExam import BmExam
from application import db


route_baoming = Blueprint( 'baoming_page',__name__ )


@route_baoming.route( "/index", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        resp_data = {}
        req = request.args  # 参数多时用values ,参数少时用args
        examid = int(session.get("examid"))
        # reback_url = UrlManager.buildUrl("/examset/index")

        info = BmExam.query.filter_by(exam_id=examid).first()

        if info:
            x_rules = info.x_rules.split(',')
            new_x_rules = []
            for i in x_rules:
                new_x_rules.append(int(i))

            m_rules = info.m_rules.split(',')
            new_m_rules = []
            for i in m_rules:
                new_m_rules.append(int(i))
            xstart = min(new_x_rules)
            xend = max(new_x_rules)
            mstart = min(new_m_rules)
            mend = max(new_m_rules)
            resp_data['xstart'] = xstart
            resp_data['xend'] = xend
            resp_data['mstart'] = mstart
            resp_data['mend'] = mend

        resp_data['info'] = info
        resp_data['current'] = 'index'
        return ops_render( "baoming/index.html", resp_data )

    # post
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                     # 参数多时用values ,参数少时用args
    examid = req['examid'] if 'examid' in req else 0                 # 获取当前关联考试id
    exam_name = req['exam_name'] if 'exam_name' in req else ''   # 关联考试名称
    show_name = req['show_name'] if 'show_name' in req else ''   # 报名名称
    neednum = req['neednum'] if 'neednum' in req else 0          # 所需人数
    beizhu = req['beizhu'] if 'beizhu' in req else ''            # 备注说明
    rule_status = req['rule_status'] if 'rule_status' in req else 0  #
    status = req['status'] if 'status' in req else 0                 #
    rule_status = 1 if rule_status == "true" else 0
    status = 1 if status == "true" else 0

    # 报名条件
    xstart = req['xstart'] if 'xstart' in req else 0            # X起始编号
    xend = req['xend'] if 'xend' in req else 0                  # X结束编号
    mstart = req['mstart'] if 'mstart' in req else 0            # M起始编号
    mend = req['mend'] if 'mend' in req else 0                  # M结束编号

    x_rules = list(range(int(xstart),int(xend)+1))              # 将x规则补全
    m_rules = list(range(int(mstart),int(mend)+1))              # 将m规则补全

    info_x_rules = ""
    for i in x_rules:
        info_x_rules = info_x_rules + str(i) + ","              # 列表转字符串
    info_x_rules = info_x_rules[:-1]                            # 去掉字符串最后一位多的“，”

    info_m_rules = ""
    for ii in m_rules:
        info_m_rules = info_m_rules + str(ii) + ","             # 列表转字符串
    info_m_rules = info_m_rules[:-1]                            # 去掉字符串最后一位多的“，”

    bmexam_info = BmExam.query.filter_by(exam_id=examid).first()  # 查出数据库中的信息
    if bmexam_info:         # 如果存在
        model_bmexam_info = bmexam_info
    else:                   # 如果不存在
        model_bmexam_info = BmExam()
        model_bmexam_info.created_time = getCurrentDate()

    model_bmexam_info.exam_id = int(examid)
    model_bmexam_info.exam_name = exam_name
    model_bmexam_info.show_exam_name = show_name
    model_bmexam_info.x_rules = info_x_rules
    model_bmexam_info.m_rules = info_m_rules
    model_bmexam_info.numbers = int(neednum)
    model_bmexam_info.beizhu = beizhu
    model_bmexam_info.rule_status = rule_status
    model_bmexam_info.status = status

    model_bmexam_info.updated_time = getCurrentDate()

    # 提交信息
    try:
        db.session.add(model_bmexam_info)
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()

    return jsonify(resp)

