# -*- coding: utf-8 -*-
# 接受小程序用户登录操作

from web.controllers.api import route_api
from flask import request, jsonify, g
from application import app, db
import requests, json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import MemberService
from common.models.food.WxShareHistory import WxShareHistory
from common.models.member.MemberPeopleBind import MemberPeopleBind
from common.models.people.People import People


# 授权登录接口
@route_api.route("/member/login", methods=["GET", "POST"])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)
    # app.logger.info(req)
    # 使用code 向微信官方获取openid
    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)

    nickname = req['nickName'] if 'nickName' in req else ''
    sex = req['gender'] if 'gender' in req else ''
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ''
    '''
       判断是否已经测试过，注册了直接返回一些信息
    '''
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:                     # 如果没有注册
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            resp['code'] = -1
            resp['msg'] = "提交数据库出错"
            db.session.rollback()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ''                   # 扩展字段
        model_bind.updated_time = model_bind.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return jsonify(resp)

# 判断是否已注册
@route_api.route("/member/check-reg", methods=["GET", "POST"])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''    # 获取code
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return jsonify(resp)

        # 使用code 向微信官方获取openid
    openid = MemberService.getWeChatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用微信出错"
        return jsonify(resp)
    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()  # 用openid 判断是注册库中有没有此账号
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未绑定"
        return jsonify(resp)
    member_info = Member.query.filter_by(id=bind_info.member_id).first()   # 查出库中用户信息
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查询到绑定信息"
        return jsonify(resp)

    token = "%s#%s"%( MemberService.geneAuthCode(member_info), member_info.id )
    resp['data'] = {'token': token}
    return jsonify(resp)

# my/index 接口 查询是否绑定，返回用户昵称、头像
@route_api.route("/member/my", methods=["GET"])
def myIndex():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    # 获取member信息
    auth_cookie = request.headers.get("Authorization")
    if auth_cookie is None:
        return False
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False
    member_info = Member.query.filter_by(id=auth_info[1]).first()
    resp['data']['bind_flag'] = True    # 默认绑定

    # 获取绑定信息
    try:
        bind_info = MemberPeopleBind.query.filter_by(member_id=auth_info[1]).first()
    except Exception:
        return False
    if bind_info is None:
        resp['data']['bind_flag'] = False      # 未绑定

    resp['data']['info'] = {
        'name':member_info.nickname,
        'avatar':member_info.avatar
    }
    return jsonify(resp)

# 绑定操作接口
@route_api.route("/member/bind", methods=["GET"])
def memberBind():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    # 获取member信息
    auth_cookie = request.headers.get("Authorization")
    if auth_cookie is None:
        return False
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False
    member_id = auth_info[1]
    # 获取绑定信息
    try:
        bind_info = MemberPeopleBind.query.filter_by(member_id=member_id).first()
    except Exception:
        return False
    if bind_info:
        resp['code'] = -1
        resp['msg'] = "当前微信已绑定，不要重复绑定"
        return jsonify(resp)
    # 人员信息
    people_name = req['name'] if 'name' in req else ''
    people_info = People.query.filter_by(name=people_name).first()
    if not people_info:
        resp['code'] = -1
        resp['msg'] = "当前姓名不存在，请联系系统管理员录入"
        return jsonify(resp)

    bind_info = MemberPeopleBind()   # 实例化新的绑定关系对象
    bind_info.member_id = member_id
    bind_info.people_id = people_info.id
    bind_info.beizhu1 = people_name
    bind_info.created_time = getCurrentDate()
    bind_info.updated_time = getCurrentDate()
    # 提交信息
    try:
        db.session.add(bind_info)
        db.session.commit()
    except Exception as e:
        print(e)
        resp['code'] = -1
        resp['msg'] = "提交数据库出错"
        db.session.rollback()
    return jsonify(resp)


# 用户页面分享 记录
# @route_api.route("/member/share", methods=["GET", "POST"])
# def share():
#     resp = {'code': 200, 'msg': '操作成功', 'data': {}}
#     req = request.values
#     url = req['url'] if 'url' in req else ''
#     member_info = g.member_info
#     model_share = WxShareHistory()   # 初始化实例对象
#     if member_info:
#         model_share.member_id = member_info.id
#     model_share.share_url = url
#     model_share.created_time = getCurrentDate()
#     db.session.add(model_share)
#     try:
#         db.session.commit()
#     except Exception as e:
#         print(e)
#         resp['code'] = -1
#         resp['msg'] = "提交分享数据入数据库出错"
#         db.session.rollback()




