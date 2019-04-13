from tool.some_tool import SomeTool

class CommentTool:
    @staticmethod
    def get_comment(db, contentId):
        # 获取评论列表
        cursor = db.cursor()
        sql = 'SELECT cm.email, cm.comment, cm.created, t.userId, cm.id, c.id FROM comment cm, content c, title t ' \
              'WHERE cm.contentId = {} AND c.titleId = t.id AND c.id = {} AND cm.hidden = 0 ' \
              'ORDER BY cm.id DESC'.format(contentId, contentId)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results

    @staticmethod
    def add_comment(db, contentId, email, comment):
        # 新增评论
        cursor = db.cursor()
        sql = 'INSERT INTO comment (email, comment, contentId, created, hidden) VALUES ' \
              '("{}", \'{}\', {}, "{}", 0)'.format(email, str(comment).replace('\'', '"'), contentId, SomeTool.current_date())
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False

    @staticmethod
    def delete_comment(db, commentId):
        # 删除评论
        cursor = db.cursor()
        sql = 'UPDATE comment SET hidden = 1 WHERE id = {}'.format(commentId)
        cursor.execute(sql)
        cursor.close()
        try:
            db.commit()
            return True
        except:
            db.rollback()
            return False