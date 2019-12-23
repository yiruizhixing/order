from flask import g, render_template
import datetime

'''
自定义分页类
'''
def iPagination( params ):
    import math

    ret = {
        "is_prev":1,     # 是否有上一页
        "is_next":1,     # 是否有下一页
        "from" :0 ,
        "end":0,
        "current":0,     # 当前页号
        "total_pages":0,  # 总计页数
        "page_size" : 0,  # 每一页的大小
        "total" : 0,      # 总记录数
        "url":params['url']
    }

    total = int( params['total'] )
    page_size = int( params['page_size'] )
    page = int( params['page'] )
    display = int( params['display'] )
    total_pages = int( math.ceil( total / page_size ) )
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0

    semi = int( math.ceil( display / 2 ) )

    if page - semi > 0 :
        ret['from'] = page - semi
    else:
        ret['from'] = 1

    if page + semi <= total_pages :
        ret['end'] = page + semi
    else:
        ret['end'] = total_pages

    ret['current'] = page
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    ret['range'] = range( ret['from'],ret['end'] + 1 )
    return ret




'''
统一渲染方法
'''
def ops_render(template,context = {}):
    if 'current_user'in g:
        context['current_user'] = g.current_user
    return render_template(template, **context)

'''
获取当前时间
'''
def getCurrentDate( format = "%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime( format )        # 返回当前时间并格式化，需要引用datetime模块