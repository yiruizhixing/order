# 基础环境配置
SERVER_PORT = 8999
DEBUG = False
SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME = "imooc_food"

APP = {
    'domain':"http://192.168.244.6:8999"
}

# 过滤url 不验证登录状态
IGNORE_URLS = [
    "^/user/login",
    "^/api",
    "^/exam/choose"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]


PAGE_SIZE = 50    # 分页配置，每页显示条数
PAGE_DISPLAY = 10  # 显示页数

# 用户账号状态
STATUS_MAPPING = {
    "1":"正常",
    "0":"已删除"
}


# 小程序参数
MINA_APP = {
    'appid': 'wx21ff50521f0e437a',
    'appkey': '12cf2ebf0ae711a1c5ef06a7cda37300'
}


UPLOAD = {
    'ext':['jpg','gif','bmp','jpeg','png'],
    'prefix_path':'/static/upload/',
    'prefix_url':'/static/upload/'
}

# 设置SECRET_KEY   session 加密用
SECRET_KEY = "fhdk^fk#djefkj&*&*&"

