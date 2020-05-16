# 这里是： 生成和用户相关的信息的方法库
import string, random, hashlib,base64


class UserService:

    #  设置coolie的value的第一个字段是： 通过下面md5混合多个字段进行加密后的md5字段
    @staticmethod
    def geneAuthCode(user_info=None):
        m = hashlib.md5()
        str = "%s-%s-%s-%s-%s" % (user_info.usr_id, user_info.login_name, user_info.login_pwd,
                                  user_info.login_salt, user_info.status)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    # 产生加密后的密码
    @staticmethod
    def genePwd(pwd, salt):
        # 先base64加密
        str_base64 = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        md5er = hashlib.md5()       # md5 加密
        md5er.update(str_base64.encode("utf-8"))
        # 返回md5 值
        return md5er.hexdigest()

    # 产生加密用的 随机码 salt
    @staticmethod
    def genSalt(length = 16):
        saltList = [random.choice(string.ascii_letters + string.digits) for i in range(length)]
        # str = "-";
        # seq = ("a", "b", "c"); # 字符串序列
        # print str.join( seq );
        return "".join(saltList)




