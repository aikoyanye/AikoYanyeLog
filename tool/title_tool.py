from tool.some_tool import SomeTool

class TitleTool:
    @staticmethod
    def add_title(db, title, hidden, userId):
        # 添加分类
        cursor = db.cursor()
        sql = 'INSERT INTO title (title, userId, created, hidden) VALUES (\'{}\', {}, "{}", {})' \
              ''.format(str(title).replace('\'', '"'), userId, SomeTool.current_date(), hidden)
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False

    @staticmethod
    def get_titles(db, userId):
        # 获取分类，分类user的以及其他人的
        results = {}
        cursor = db.cursor()
        sql = 'SELECT t.title, t.created, u.username, t.id FROM title t, user u WHERE t.userId = {} ' \
              'AND t.userId = u.id AND t.hidden != 2 ORDER BY t.created DESC'.format(userId)
        cursor.execute(sql)
        results['user'] = cursor.fetchall()
        sql = 'SELECT t.title, t.created, u.username, t.id FROM title t, user u WHERE t.userId != {} AND ' \
              't.hidden = 0 AND t.userId = u.id ORDER BY t.created DESC'.format(userId)
        cursor.execute(sql)
        results['guest'] = cursor.fetchall()
        cursor.close()
        return results

    @staticmethod
    def edit_title(db, titleId, title, hidden):
        cursor = db.cursor()
        sql = 'UPDATE title SET title = "{}", hidden = {} WHERE id = {}'.format(title, hidden, titleId)
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False

    @staticmethod
    def delete_title(db, titleId):
        cursor = db.cursor()
        sql = 'UPDATE title SET hidden = 2 WHERE id = {}'.format(titleId)
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False

    @staticmethod
    def get_titles_for_content(db, userId):
        # 新增content时获取用户的title
        cursor = db.cursor()
        sql = 'SELECT id, title FROM title WHERE userId = {}'.format(userId)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result