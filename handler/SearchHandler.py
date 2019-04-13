import tornado.web, json
from tool.some_tool import SomeTool

class SearchHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        # 返回搜索结果
        self.write(json.dumps(SomeTool.search(self.application.db, self.get_argument('key'), self.get_argument('userId'))))