# 基础环境配置
SERVER_PORT = 8999
DEBUG = False
SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME = "imooc_food"

# 过滤url 不验证登录状态
IGNORE_URLS = [
    "^/user/login",
    "^/api",

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
MINA_APP ={
    'appid':'wx21ff50521f0e437a',
    'appkey':'12cf2ebf0ae711a1c5ef06a7cda37300'
}