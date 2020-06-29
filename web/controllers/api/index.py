# -*- coding: utf-8 -*-
from web.controllers.api import route_api
from  flask import request,jsonify,g
from common.libs.Helper import getCurrentDate
from common.models.news.News import News
from common.models.bm.BmExam import BmExam
from common.models.bm.BmInfo import BmInfo
from common.libs.UrlManager import UrlManager
from common.models.member.Member import Member
from common.models.member.MemberPeopleBind import MemberPeopleBind
import time, datetime
from application import db



#  首页考务通知新闻列表接口
@route_api.route("/home/news" )
def indexNews():
    resp = { 'code':200 ,'msg':'操作成功~','data':{} }

    # 新闻通知列表处理
    news_list = News.query.filter_by( status = 1).order_by(News.id.desc()).all()
    data_news_list = []
    if news_list:
        temp_i = 2               # 控制返回的新闻条数
        for item in news_list:   # 拼接构造新格式
            # print(type(item.created_time))
            temp_data={
                'id': item.id,
                'name': item.name,
                'created_time': item.created_time.strftime('%Y-%m-%d')   # 格式化时间
            }
            data_news_list.append(temp_data)
            temp_i = temp_i - 1
            if temp_i == 0:
                break

    # 报名列表处理
    bm_list = BmExam.query.filter_by(status = 1).order_by(BmExam.exam_id.desc()).all()
    data_bm_list = []
    if bm_list:
        for item in bm_list:  # 拼接构造新格式
            # print(type(item.created_time))
            temp_data = {
                'id': item.id,
                'title': item.show_exam_name,
                'created_time': item.created_time.strftime('%Y-%m-%d')  # 格式化时间
            }
            data_bm_list.append(temp_data)

    resp['data']['news_list'] = data_news_list
    resp['data']['bm_list'] = data_bm_list
    return jsonify( resp )

# 新闻内容接口--考务通知内容
@route_api.route("/news/info" )
def newsInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    news_info = News.query.filter_by( id = id ).first()
    if not news_info or not news_info.status :
        resp['code'] = -1
        resp['msg'] = "相关内容已下线"
        return jsonify(resp)

    resp['data']['info'] = {
        "id":news_info.id,
        "name":news_info.name,
        "summary":news_info.summary,
        'created_time': news_info.created_time.strftime('%Y-%m-%d')     # 格式化时间
    }
    return jsonify(resp)

# 巡考报名项目内容返回接口
@route_api.route("/bm/info" )
def bmInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    # 获取报名项目规则信息
    id = int(req['id']) if 'id' in req else 0          # 报名项目id
    bm_exam = BmExam.query.filter_by( id = id ).first()
    if not bm_exam or not bm_exam.status :
        resp['code'] = -1
        resp['msg'] = "相关报名已关闭"
        return jsonify(resp)

    x_rules = bm_exam.x_rules.split(',')
    new_x_rules = []
    for i in x_rules:
        new_x_rules.append(int(i))
    m_rules = bm_exam.m_rules.split(',')
    new_m_rules = []
    for i in m_rules:
        new_m_rules.append(int(i))
    xstart = min(new_x_rules)
    xend = max(new_x_rules)
    mstart = min(new_m_rules)
    mend = max(new_m_rules)

    xrules = "X" + str(xstart) + "--X" + str(xend)
    mrules = "M" + str(mstart) + "--M" + str(mend)

    # 获取member信息
    auth_cookie = request.headers.get("Authorization")
    if auth_cookie is None:
        return False
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    try:
        bind_info = MemberPeopleBind.query.filter_by(member_id=auth_info[1]).first()
    except Exception:
        return False
    if bind_info is None:
        resp['code'] = -1
        resp['msg'] = "未绑定信息，请先到个人中心进行绑定操作"
        return jsonify(resp)

    # 获取用户是否已报名信息
    bm_info = BmInfo.query.filter(BmInfo.bm_exam_id == id and BmInfo.people_id == bind_info.people.xunkao_id).first()  # 查询是否已存在报名信息
    shenhe_dic = {'1': '审核通过', '2': '审核未通过', '3': '未审核', '4': '无'}
    if bm_info:
        resp['data']['bm_status'] = "已报名"
        resp['data']['sh_status'] = shenhe_dic.get(str(bm_info.sh_status), "无")
    else:
        resp['data']['bm_status'] = "未报名"
        resp['data']['sh_status'] = "无"

    resp['data']['info'] = {
        "id":bm_exam.id,                       # 报名项目id
        "title":bm_exam.show_exam_name,        # 报名项目名称
        "numbers":bm_exam.numbers,             # 需求人数
        "beizhu": bm_exam.beizhu,              # 备注
        "xrules": xrules,
        "mrules": mrules,
        "name":bind_info.people.name,          # 人员姓名
        "people_id": bind_info.people_id,      # 人员id
        "bianhao":bind_info.people.xunkao_id,  # 巡考编号
        'created_time': bm_exam.created_time.strftime('%Y-%m-%d')     # 格式化时间
    }
    return jsonify(resp)


# 巡考报名信息提交接口
@route_api.route("/bm/post", methods=["POST"] )
def bmPost():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0   # 报名项目id
    name = req['name'] if 'name' in req else '' # 人员姓名
    people_id = req['people_id'] if 'people_id' in req else 0  # 人员id
    bianhao = req['bianhao'] if 'bianhao' in req else ''       # 巡考编号

    bm_exam = BmExam.query.filter_by(id=id).first()           # 查询报名项目信息
    if not bm_exam or not bm_exam.status:
        resp['code'] = -1
        resp['msg'] = "相关报名已关闭"
        return jsonify(resp)
    if people_id is None or name is None:
        resp['code'] = -1
        resp['msg'] = "未绑定信息，请先到个人中心进行绑定操作~"
        return jsonify(resp)

    if bm_exam.rule_status == 1:    # 如果开启报名条件验证
        x_rules = bm_exam.x_rules.split(',')
        new_x_rules = []
        for i in x_rules:
            new_x_rules.append(int(i))
        m_rules = bm_exam.m_rules.split(',')
        new_m_rules = []
        for i in m_rules:
            new_m_rules.append(int(i))

        bianhao_number =int(bianhao[1:])   # 取编号X058的数字部分转为int 58

        if bianhao_number not in new_x_rules and bianhao_number not in new_m_rules:  # 报名条件验证
            resp['code'] = -1
            resp['msg'] = "不符合本次报名条件~"
            return jsonify(resp)

    bm_info = BmInfo.query.filter(BmInfo.bm_exam_id == id and BmInfo.people_id == people_id ).first()   # 查询是否已存在报名信息
    if bm_info:
        resp['code'] = -1
        resp['msg'] = "请不要重复报名"
        return jsonify(resp)
    bm_info = BmInfo()
    bm_info.bm_exam_id = id
    bm_info.people_id = people_id
    bm_info.name = name
    bm_info.xunkao_id = bianhao
    bm_info.status = 1
    bm_info.sh_status = 1
    bm_info.kaodian_id = 0
    bm_info.created_time = getCurrentDate()
    bm_info.updated_time = getCurrentDate()

    # 提交信息
    try:
        db.session.add(bm_info)
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()

    return jsonify(resp)