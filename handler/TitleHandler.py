import tornado.web, json
from handler.BaseHandler import BaseHandler
from tool.title_tool import TitleTool

class TitleHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # 获取title列表，根据userId获取
            self.write(json.dumps(TitleTool.get_titles(self.application.db, self.get_argument('userId'))))
        elif self.get_argument('type') == '2':
            # 新增content时获取用户的title
            self.write(json.dumps(TitleTool.get_titles_for_content(self.application.db, self.get_argument('userId'))))

    async def post(self, *args, **kwargs):
        # 新建title
        TitleTool.add_title(self.application.db, self.get_argument('title'), self.get_argument('hidden'),
                            self.get_argument('userId'))

    async def put(self, *args, **kwargs):
        # 编辑标题
        TitleTool.edit_title(self.application.db, self.get_argument('titleId'), self.get_argument('title'),
                             self.get_argument('hidden'))

    async def delete(self, *args, **kwargs):
        # 删除标题
        TitleTool.delete_title(self.application.db, self.get_argument('titleId'))