import datetime, hashlib, os, shutil

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

    @staticmethod
    def search(db, key, userId):
        # 返回查询结果
        keys = str(key).split('%')
        results = {}
        cursor = db.cursor()
        sql = 'SELECT t.title, t.created, u.username, t.id FROM title t, user u WHERE t.userId = {} ' \
              'AND t.userId = u.id AND t.hidden != 2'.format(userId)
        sql1 = 'SELECT t.title, t.created, u.username, t.id FROM title t, user u WHERE t.userId != {} AND ' \
               't.hidden = 0 AND t.userId = u.id'.format(userId)
        sql2 = 'SELECT c.head, c.created, c.id, t.id FROM content c, title t, user u WHERE ' \
               'c.titleId = t.id AND t.userId = u.id AND u.id = {} AND c.hidden != 2'.format(userId)
        sql3 = 'SELECT c.head, c.created, c.id, t.id FROM content c, title t, user u WHERE ' \
               'c.titleId = t.id AND t.userId = u.id AND u.id != {} AND c.hidden = 0'.format(userId)
        for key in keys:
            sql = sql + ' AND t.title like "%{}%"'.format(key)
            sql1 = sql1 + ' AND t.title like "%{}%"'.format(key)
            sql2 = sql2 + ' AND c.head like "%{}%"'.format(key)
            sql3 = sql3 + ' AND c.head like "%{}%"'.format(key)
        sql = sql + ' ORDER BY t.id DESC'
        sql1 = sql1 + ' ORDER BY t.id DESC'
        sql2 = sql2 + ' ORDER BY t.id DESC'
        sql3 = sql3 + ' ORDER BY t.id DESC'
        cursor.execute(sql)
        results['user'] = cursor.fetchall()
        cursor.execute(sql1)
        results['guest'] = cursor.fetchall()
        cursor.execute(sql2)
        results['ucontent'] = cursor.fetchall()
        cursor.execute(sql3)
        results['gcontent'] = cursor.fetchall()
        return results

    @staticmethod
    def add_ip(db, ip):
        # 添加ban ip
        cursor = db.cursor()
        sql = 'INSERT INTO ban_ip (ip) VALUES ("{}")'.format(ip)
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False