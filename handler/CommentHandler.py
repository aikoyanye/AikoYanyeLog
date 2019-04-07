import tornado.web, json
from tool.comment_tool import CommentTool

class CommentHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        # 获取评论列表
        self.write(json.dumps(CommentTool.get_comment(self.application.db, self.get_argument('contentId'))))

    async def post(self, *args, **kwargs):
        # 新增评论
        CommentTool.add_comment(self.application.db, self.get_argument('contentId'), self.get_argument('email'),
                                                self.get_argument('comment'))

    async def delete(self, *args, **kwargs):
        # 删除评论
        CommentTool.delete_comment(self.application.db, self.get_argument('commentId'))