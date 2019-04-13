from tool.some_tool import SomeTool
import os

class MainTool:
    @staticmethod
    def register(db, email, username, password):
        # 注册普通用户
        cursor = db.cursor()
        sql = 'INSERT INTO user ("email", "username", "password", "type", "created") VALUES ' \
              '("{}", "{}", "{}", "normal", "{}")'.format(email, username, SomeTool.key(password), SomeTool.current_date())
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return MainTool.login(db, email, password)
        except:
            db.rollback()
            return False

    @staticmethod
    def login(db, email, password):
        # 登录
        cursor = db.cursor()
        sql = 'SELECT id FROM user WHERE email = "{}" AND password = "{}"' \
              ''.format(email, SomeTool.key(password))
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result if result != None else False

    @staticmethod
    def change_info(db, email, username, oldpassword, password):
        # 修改用户信息
        cursor = db.cursor()
        sql = 'SELECT id FROM user WHERE password = "{}"'.format(SomeTool.key(oldpassword))
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None: return False
        sql = 'UPDATE user SET email = "{}", username = "{}", password = "{}" WHERE id = {}' \
              ''.format(email, username, SomeTool.key(password), int(result[0]))
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False

    @staticmethod
    def user_by(db, id):
        cursor = db.cursor()
        sql = 'SELECT email, username, id, type FROM user WHERE id = {}'.format(id)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    @staticmethod
    def update_list(db):
        cursor = db.cursor()
        sql = 'SELECT version, content, created FROM update_list ORDER BY id DESC'
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    @staticmethod
    def post_update(db, version, content):
        cursor = db.cursor()
        sql = 'INSERT INTO update_list (version, content, created) VALUES ("{}", \'{}\', "{}")' \
              ''.format(version, str(content).replace('\'', '"'), SomeTool.current_date())
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False

    @staticmethod
    def bg_pic(pic):
        if os.path.exists('static/bg.png'):
            os.remove('static/bg.png')
        with open('static/bg.png', 'wb') as bg:
            bg.write(pic)

    @staticmethod
    def add_notice(db, content):
        cursor = db.cursor()
        sql = 'INSERT INTO notice (content, created) VALUES (\'{}\', "{}")'.format(str(content).replace('\'', '"'), SomeTool.current_date())
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False

    @staticmethod
    def get_notice(db):
        cursor = db.cursor()
        sql = 'SELECT content FROM notice ORDER BY id DESC'
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result