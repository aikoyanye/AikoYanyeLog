import tornado.web, json
from tool.some_tool import SomeTool
from handler.BaseHandler import BaseHandler

class SearchHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        # 返回搜索结果
        self.write(json.dumps(SomeTool.search(self.application.db, self.get_argument('key'), self.get_argument('userId'))))

    async def post(self, *args, **kwargs):
        # 添加 ban ip
        SomeTool.add_ip(self.application.db, self.get_argument('ip'))