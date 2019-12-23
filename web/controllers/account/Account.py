# -*- coding: utf-8 -*-
from flask import Blueprint, request, redirect, jsonify
from common.libs.Helper import ops_render, iPagination, getCurrentDate            # iPagination为统一分页方法类
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.User import User
from common.models.log.AppAccesslog import AppAccessLog
from sqlalchemy import or_

from application import app, db
route_account = Blueprint( 'account_page',__name__ )


@route_account.route( "/index" )
def index():
    resp_data = {}
    req = request.values
    page = int( req['p']) if ( 'p' in req and req['p'] ) else 1    # 当前页号，默认为1

    query = User.query

    # 用户搜索处理
    if 'mix_kw' in req:
        rule = or_( User.nickname.ilike("%{0}%".format(req['mix_kw'])), User.mobile.ilike("%{0}%".format(req['mix_kw'])) )        # 需要导入 sqlalchemy import or_   or 查询
        # ilike 不区分大小写 对用户名或手机号查询 or为混合查询
        query = query.filter(rule)
    # 用户账号有效无效查询
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))

    # 分页参数
    page_params = {
        'total': query.count(),                 # 统计账号总数
        'page_size': app.config['PAGE_SIZE'],   # 每页显示账号数
        'page': page,
        'display': app.config['PAGE_DISPLAY'],  # 展示总页数
        'url': request.full_path.replace("&p={}".format(page), "")
    }
    pages = iPagination( page_params )         # 分页操作
    offset = ( page - 1 ) * app.config['PAGE_SIZE']    # 偏移量，第二页从50开始，第三页从101开始
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by( User.uid.desc() ).all() [ offset:limit]     # 使用uid字段倒序排  # .all()  为取出所有的数据 然后存到列表list
    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req                   #搜索框内容
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render( "account/index.html", resp_data )      # 将resp_data作为参数，用json传递给模板页面


# #账户详情
@route_account.route( "/info" )
def info():
    resp_data = {}
    req = request.args                     # args为取get参数
    uid = int (req.get('id', 0))
    reback_url = UrlManager.buildUrl("/account/index")
    if uid < 1:
        return redirect( reback_url )

    info = User.query.filter_by( uid = uid ).first()
    if not info:   # 如果查不到相关信息 ，跳到首页
        return redirect( reback_url )
    resp_data['info'] = info

    # 查询取出用户访问日志，时间倒序排列
    querylog = AppAccessLog.query.filter_by( uid = uid ).order_by(AppAccessLog.created_time.desc()).all()

    resp_data['querylog'] = querylog
    return ops_render( "account/info.html", resp_data )  # 将resp_data作为参数，用json传递给模板页面


# 新增账号,编辑账号
@route_account.route( "/set",methods = ["GET","POST"] )
def set():
    default_pwd = "******"                                  # 默认密码
    if request.method == "GET":
        resp_data = {}
        req = request.args                                  # 参数少时用args
        uid = int( req.get( "id", 0 ) )                     # 获取当前id
        info = None
        if uid:                                             # 如果uid存在,说明进入的是编辑账号页面，否则进入的是新增账号页面
            info = User.query.filter_by( uid = uid ).first()  # 前端页面显示当前用户信息
        resp_data['info'] = info                            # 把当前登录账户信息返回前端显示
        return ops_render( "account/set.html", resp_data)

    # 下面是POST处理
    resp = {'code': 200, 'msg': '操作成功', 'data': ''}
    req = request.values                                    # 参数多时用values ,参数少时用args
    id = req['id'] if 'id' in req else 0                    # 获取当前用户id
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    email = req['email'] if 'email' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名"
        return jsonify(resp)
    if mobile is None or len(mobile) < 11:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的手机号码"
        return jsonify(resp)
    if email is None or len(email) < 5:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的邮箱"
        return jsonify(resp)
    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录用户名"
        return jsonify(resp)
    if login_pwd is None or len(login_pwd) < 6:
        resp['code'] = -1
        resp['msg'] = "密码过短"
        return jsonify(resp)

    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()  # 判断新增的用户名是否已存在
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该登录名已存在~"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if user_info:                                           # 如果存在,说明进入的是编辑账号页面，否则进入的是新增账号页面
        model_user = user_info
        if login_pwd != default_pwd:                        # 如果前端传来的密码不为6个*，则进行密码修改
            model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)  # 需要导入UserService
    else:                                                   # 新增
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.geneSalt()      # 生成加密密钥
        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)      # 需要导入UserService

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    model_user.updated_time = getCurrentDate()

    # 提交信息
    db.session.add(model_user)
    db.session.commit()
    return jsonify(resp)


# 删除恢复用户操作
@route_account.route("/ops",methods = ["POST"])
def ops():
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

    user_info = User.query.filter_by(uid=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在，请重试"
        return jsonify(resp)
    if act == "remove":
        user_info.status = 0
    elif act =="recover":
        user_info.status = 1

    # 提交信息
    user_info.update_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)
