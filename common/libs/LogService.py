from flask import request, g
from application import app, db
import json
from common.models.log.AppAccesslog import AppAccessLog
from common.models.log.AppErrorlog import AppErrorLog
from common.libs.Helper import getCurrentDate

class LogService():
    # 访问日志获取、入库处理
    @staticmethod
    def addAccessLog():
        target = AppAccessLog()
        target.target_url = request.url   # 获取当前的url地址
        target.referer_url = request.referrer
        target.ip = request.remote_addr  # 访客ip
        target.query_params = json.dumps( request.values.to_dict())
        if 'current_user' in g and g.current_user is not None:
            target.uid = g.current_user.uid
        target.ua = request.headers.get("User-Agent")
        target.created_time = getCurrentDate()  # 获取时间
        db.session.add(target)  # 提交入库
        db.session.commit()
        return True



    # 错误日志处理
    @staticmethod
    def addErrorLog(content):
        target = AppErrorLog()
        target.target_url = request.url  # 获取当前的url地址
        target.referer_url = request.referrer
        target.query_params = json.dumps(request.values.to_dict())
        target.content = content
        target.created_time = getCurrentDate()  # 获取时间
        db.session.add(target)  # 提交入库
        db.session.commit()
        return True

