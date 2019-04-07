import datetime, hashlib

class SomeTool:
    @staticmethod
    def get_login_status(current, cookie):
        # 获取登录状态，每次请求都对比cookie和当前登录信息是否一致
        return True if str(current) == str(cookie) else False

    @staticmethod
    def current_date():
        # 返回当前时间
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def key(emm):
        # 将密码存储为md5
        m = hashlib.md5()
        m.update(str(emm).encode('utf-8'))
        return m.hexdigest()