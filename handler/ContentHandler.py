import tornado.web, json
from tool.content_tool import ContentTool

class ContentHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # 获取content list
            self.write(json.dumps(ContentTool.content_list(self.application.db, self.get_argument('titleId'),
                                                           self.get_argument('userId'))))
        elif self.get_argument('type') == '2':
            # 获取某个content
            self.write(json.dumps(ContentTool.get_content(self.application.db, self.get_argument('contentId'))))

    async def post(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # 上传图片
            self.write(json.dumps(ContentTool.upload_pic(self.request.files.get('pic')[0]['body'],
                                                                   self.get_argument('username'))))
        elif self.get_argument('type') == '2':
            # 新增文章
            ContentTool.add_content(self.application.db, self.get_argument('titleId'), self.get_argument('head'),
                                    self.get_argument('content'), self.get_argument('hidden'))

    async def put(self, *args, **kwargs):
        # 修改content
        self.write(json.dumps(ContentTool.edit_content(self.application.db, self.get_argument('contentId'),
                                        self.get_argument('head'), self.get_argument('titleId'),
                                                       self.get_argument('content'), self.get_argument('hidden'))))

    async def delete(self, *args, **kwargs):
        # 删除content
        ContentTool.delete_content(self.application.db, self.get_argument('contentId'))