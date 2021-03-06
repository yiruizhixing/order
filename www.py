from application import app
from web.controllers.index import route_index
from web.controllers.user.User import route_user
from web.controllers.account.Account import route_account
from web.controllers.finance.Finance import route_finance
from web.controllers.food.Food import route_food
from web.controllers.people.People import route_people
from web.controllers.member.Member import route_member
from web.controllers.stat.Stat import route_stat
from web.controllers.api import route_api
from web.controllers.upload.upload import route_upload
from web.controllers.exam.Exam import route_exam
from web.controllers.kaowu.Kaowu import route_kaowu
from web.controllers.examset.Examset import route_examset
from web.controllers.baoming.Baoming import route_baoming
from web.controllers.peixun.Peixun import route_peixun
from web.controllers.news.News import route_news

'''
统一拦截器and 统一错误处理
'''
from web.interceptors.AuthInterceptor import *
from web.interceptors.ApiAuthInterceptor import *
from web.interceptors.ErrorInterceptor import *

'''
蓝图功能，对所有的url进行蓝图功能配置
'''
app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_user, url_prefix="/user")
app.register_blueprint(route_account, url_prefix="/account")
app.register_blueprint(route_finance, url_prefix="/finance")
app.register_blueprint(route_food, url_prefix="/food")
app.register_blueprint(route_people, url_prefix="/people")
app.register_blueprint(route_member, url_prefix="/member")
app.register_blueprint(route_stat, url_prefix="/stat")
app.register_blueprint(route_api, url_prefix="/api")
app.register_blueprint(route_upload, url_prefix="/upload")
app.register_blueprint(route_exam, url_prefix="/exam")
app.register_blueprint(route_kaowu, url_prefix="/kaowu")
app.register_blueprint(route_examset, url_prefix="/examset")
app.register_blueprint(route_baoming, url_prefix="/baoming")
app.register_blueprint(route_peixun, url_prefix="/peixun")
app.register_blueprint(route_news, url_prefix="/news")

