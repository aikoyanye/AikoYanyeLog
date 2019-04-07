from tool.some_tool import SomeTool

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
        sql = 'SELECT email, username, id FROM user WHERE email = "{}" AND password = "{}"' \
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