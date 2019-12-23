# 错误访问拦截器
from application import app
from common.libs.Helper import ops_render
from common.libs.LogService import LogService

# 404错误处理
@app.errorhandler(404)
def error_404(e):
    LogService.addErrorLog(str(e))  # 将e 以字符串形式传入处理, 入库操作
    return ops_render('error/error.html', {'status':404,'msg':"很抱歉，您访问的页面不存在"})