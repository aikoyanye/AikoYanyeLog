from tool.some_tool import SomeTool

class ContentTool:
    @staticmethod
    def upload_pic(pic, username):
        # 上传图片
        filename = 'static/resource/pic/' + username + SomeTool.current_date().replace(':', '-') + '.png'
        with open(filename, 'wb', ) as file:
            file.write(pic)
        return filename

    @staticmethod
    def add_content(db, titleId, head, content, hidden):
        cursor = db.cursor()
        sql = 'INSERT INTO content (head, content, titleId, created, hidden) VALUES ' \
              '(\'{}\', \'{}\', \'{}\', \'{}\', {})' \
              ''.format(str(head).replace('\'', '"'), str(content).replace('\'', '"'), titleId, SomeTool.current_date(), hidden)
        print(sql)
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False

    @staticmethod
    def content_list(db, titleId, userId):
        cursor = db.cursor()
        sql = 'SELECT id FROM title WHERE id = {} AND userId = {}'.format(titleId, userId)
        cursor.execute(sql)
        if cursor.fetchone():
            sql = 'SELECT head, created, id FROM content WHERE titleId = {} AND hidden != 2 ' \
                  'ORDER BY created DESC'.format(titleId)
        else:
            sql = 'SELECT head, created, id FROM content WHERE titleId = {} AND hidden = 0 ' \
                  'ORDER BY created DESC'.format(titleId)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    @staticmethod
    def get_content(db, contentId):
        cursor = db.cursor()
        sql = 'SELECT c.head, c.content, c.created, t.title, t.userId FROM content c, title t ' \
              'WHERE t.id = c.titleId AND c.id = {}'.format(contentId)
        cursor.execute(sql)
        results = cursor.fetchone()
        cursor.close()
        return results

    @staticmethod
    def delete_content(db, contentId):
        cursor = db.cursor()
        sql = 'UPDATE content SET hidden = 2 WHERE id = {}'.format(contentId)
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False

    @staticmethod
    def edit_content(db, contentId, head, titleId, content, hidden):
        cursor = db.cursor()
        created = SomeTool.current_date()
        sql = 'UPDATE content SET head = \'{}\', titleId = {}, content = \'{}\', hidden = {}, created = \'{}\' ' \
              'WHERE id = {}'.format(str(head).replace('\'', '"'), titleId, str(content).replace('\'', '"'), hidden, created, contentId)
        cursor.execute(sql)
        try:
            db.commit()
            sql = 'SELECT title FROM title WHERE id = {}'.format(titleId)
            cursor.execute(sql)
            results = list(cursor.fetchone())
            results.append(created)
            cursor.close()
            return results
        except:
            db.rollback()
            cursor.close()
            return False