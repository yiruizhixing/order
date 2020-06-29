# 小程序api拦截器，

from application import app
from flask import request, redirect, g, session, jsonify
from common.models.member.Member import Member
from common.libs.member.MemberService import MemberService
import re                                       # 导入正则表达式模块

'''
api认证
'''
@app.before_request
def before_request():
    api_ignore_urls = app.config['API_IGNORE_URLS']
    path = request.path
    if "/api" not in path:        # 如果不是api请求，则不处理。
        return

    member_info = check_member_login()
    g.member_info = None

    if member_info:
        g.current_user = member_info

    # app.logger.info(g.current_exam)
    pattern = re.compile( '%s' % "|" .join(api_ignore_urls))      # 如果是不需要判断登录页面，则返回
    if pattern.match(path):
        return

    if not member_info:                                           # 如果没有登录，就返回提示
        resp = {'code': -1, 'msg': '未登录', 'data': {}}
        return jsonify(resp)


'''
判断用户是否已经登录
'''
def check_member_login():
    auth_cookie = request.headers.get("Authorization")
    # app.logger.info( auth_cookie)
    if auth_cookie is None:
        return False
    auth_info = auth_cookie.split("#")
    if len( auth_info ) != 2:
        return False

    try:
        member_info = Member.query.filter_by( id = auth_info[1] ).first()
    except Exception:
        return False
    if member_info is None:
        return False

    if auth_info[0] != MemberService.geneAuthCode( member_info ):
        return False

    if member_info.status != 1:       # 判断账号状态是否正常 1：正常，0：禁用，-1：不存在
        return False

    return member_info

