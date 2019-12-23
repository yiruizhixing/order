
import hashlib, base64, random, string


class UserService():   # 密码加密处理

    @staticmethod               # 加密cookie
    def geneAuthCode( user_info ):
        m = hashlib.md5()
        str = "%s-%s-%s-%s"%( user_info.uid,user_info.login_name,user_info.login_pwd,user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()


    @staticmethod               # 加密存储密码
    def genePwd( pwd,salt):
        m = hashlib.md5()
        str = "%s-%s" % ( base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod    # 定义静态方法
    def geneSalt( length = 16 ):   # 生成salt
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]      # 获取16位随机数 需要导入random, string
        return ( "".join(keylist) )