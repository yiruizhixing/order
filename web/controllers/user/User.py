# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, make_response, redirect, g
import json
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.Helper import ops_render
from application import app, db
from common.libs.UrlManager import UrlManager

route_user = Blueprint( 'user_page', __name__ )


@route_user.route( "/login",methods = ["GET","POST"])
def login():
    if request.method=="GET":                        # 登录页面展示
        return ops_render( "user/login.html" )
    resp = {'code':200,'msg':'登录成功','data':''}   # 定义全局变量，返回值字典，data为扩展字段
    req = request.values                             # 获取前端文本框信息
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if login_name is None or len(login_name) < 1:         # 用户名参数有效性判断
        resp['code'] = -1
        resp['msg'] = "请输入正确的登录用户名~~"
        return jsonify(resp)
    if login_pwd is None or len(login_pwd) < 1:           # 密码参数有效性判断
        resp['code'] = -1
        resp['msg'] = "请输入正确的登录密码~~"
        return jsonify(resp)
    user_info = User.query.filter_by(login_name = login_name).first()
    if not user_info:                                   # 用户名真实性判断 与数据库记录比对
        resp['code'] = -1
        resp['msg'] = "请输入正确的用户名和登录密码~1~"
        return jsonify(resp)

    if user_info.login_pwd != UserService.genePwd(login_pwd,user_info.login_salt):  # # 密码真实性判断 与数据库记录比对
        resp['code'] = -1
        resp['msg'] = "请输入正确的用户名和登录密码~2~"
        return jsonify(resp)

    if user_info.status != 1:                         # 判断用户状态是否正常
        resp['code'] = -1
        resp['msg'] = "账号异常，请联系管理员~"
        return jsonify(resp)

    response = make_response( json.dumps( resp ) )
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s"%( UserService.geneAuthCode( user_info ), user_info.uid ))
    return response


# #信息修改
@route_user.route( "/edit", methods = ["GET", "POST"])
def edit():
    if request.method == "GET":
        return ops_render( "user/edit.html",{ 'current':'edit'} )

    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                                   # 参数多时用values ,参数少时用args
    nickname = req['nickname']if'nickname'in req else ''
    email = req['email']if 'email'in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名"
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱"
        return jsonify(resp)
    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)  # 将修改好的用户信息提交到数据库
    db.session.commit()
    return jsonify(resp)


# #密码修改
@route_user.route( "/reset-pwd", methods = ["GET", "POST"])
def resetPwd():
    if request.method == "GET":
        return ops_render( "user/reset_pwd.html", {'current': 'reset-pwd'} )
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}                       # 定义全局变量，返回值字典，data为扩展字段
    req = request.values  # 获取前端文本框信息
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''

    if old_password is None or len(old_password) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的原密码~~"
        return jsonify(resp)
    if new_password is None or len(new_password) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的新密码~~"
        return jsonify(resp)
    if old_password == new_password:
        resp['code'] = -1
        resp['msg'] = "请重新输入一个新密码吧，不能和原密码相同~"
        return jsonify(resp)

    user_info = g.current_user
    if user_info.login_pwd != UserService.genePwd(old_password, user_info.login_salt):  # # 密码真实性判断 与数据库记录比对
        resp['code'] = -1
        resp['msg'] = "请输入正确的原登录密码~3~"
        return jsonify(resp)

    user_info.login_pwd = UserService.genePwd(new_password, user_info.login_salt)  # 新密码加密处理
    db.session.add(user_info)    # 加入会话
    db.session.commit()          # 提交数据库，变更操作

    '''
    更新cookie ，解决修改密码后自动退出问题
    '''
    response = make_response(json.dumps( resp ))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s"%( UserService.geneAuthCode( user_info ), user_info.uid ))
    return response


# #登出操作
@route_user.route("/logout")
def logout():  #登出操作
    response = make_response( redirect( UrlManager.buildUrl("/user/login") )) # 跳转到登录页
    response.delete_cookie( app.config['AUTH_COOKIE_NAME'])  # 清cookie
    return response