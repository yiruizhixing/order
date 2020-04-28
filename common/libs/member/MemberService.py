# 小程序注册会员 集中共用函数代码
import hashlib, base64, random, string
from application import app
import requests, json


class MemberService():   # 密码加密处理

    @staticmethod               # 加密cookie
    def geneAuthCode( member_info = None ):
        m = hashlib.md5()
        str = "%s-%s-%s"%( member_info.id, member_info.salt, member_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()


    @staticmethod    # 定义静态方法
    def geneSalt( length = 16 ):   # 生成salt
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]      # 获取16位随机数 需要导入random, string
        return ( "".join(keylist) )

    # 使用code 向微信官方获取openid
    @staticmethod
    def getWeChatOpenId(code):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code" \
            .format(app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code)
        r = requests.get(url)
        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid =res['openid']
        return openid
