import tornado.web, json
from tool.pan_tool import PanTool
from handler.BaseHandler import BaseHandler

class PanHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        self.write(json.dumps(PanTool.folder(self.get_argument('path'))))

    async def put(self, *args, **kwargs):
        PanTool.add_folder(self.get_argument('folder'), self.get_argument('current'))

    async def post(self, *args, **kwargs):
        PanTool.add_file(self.request.files.get('file')[0]['body'], self.get_argument('filename'),
                         self.get_argument('current'))

    async def delete(self, *args, **kwargs):
        PanTool.delete_files(self.get_arguments('item[]'), self.get_argument('current'))