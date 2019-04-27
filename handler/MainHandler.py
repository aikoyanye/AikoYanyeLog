import tornado.web, json, os
from tool.main_tool import MainTool
from handler.BaseHandler import BaseHandler

class MainHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        # 如果cookie有用户数据，免登录
        result = MainTool.user_by(self.application.db, self.get_cookie('id', '0'))
        if result:
            self.render('body.html', current=True, user=(result[0], result[1]), userId=result[2], type=result[3])
        else:
            self.set_cookie('id', '0')
            self.render('body.html', current=False, userId=0, user=('', ''), type='')

    async def post(self, *args, **kwargs):
        if self.get_argument('hidden') == 'info':
            if MainTool.change_info(self.application.db, self.get_argument('info_email'), self.get_argument('info_username'),
                                    self.get_argument('info_oldpassword'), self.get_argument('info_password')):
                # 修改用户信息成功
                self.redirect('/')
            else:
                self.write('<script>alert("修改失败，注意字段")</script>')
        elif self.get_argument('hidden') == 'register':
            result = MainTool.register(self.application.db, self.get_argument('register_email'), self.get_argument('register_username'),
                                 self.get_argument('register_password'))
            if result:
                # 注册成功，将信息写入cookie
                self.set_cookie('id', str(result[0]))
                if os.path.exists('static/pan/' + self.get_argument('register_username')) != True:
                    os.mkdir('static/pan/' + self.get_argument('register_username'))
                self.redirect('/')
            else:
                self.write('<script>alert("注册失败，注意字段")</script>')
                self.redirect('/')

    async def delete(self, *args, **kwargs):
        # 注销
        self.set_cookie('id', '0')

    async def put(self, *args, **kwargs):
        if self.get_argument('hidden') == 'login':
            result = MainTool.login(self.application.db, self.get_argument('login_email'), self.get_argument('login_password'))
            if result:
                # 登录
                self.set_cookie('id', str(result[0]))
                self.write('0')
            else:
                self.write(json.dumps(['1']))


class UpdateHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        self.write(json.dumps(MainTool.update_list(self.application.db)))

    async def post(self, *args, **kwargs):
        MainTool.post_update(self.application.db, self.get_argument('version'), self.get_argument('content'))

    async def put(self, *args, **kwargs):
        # 替换全局背景
        MainTool.bg_pic(self.request.files.get('bg')[0]['body'])

    async def delete(self, *args, **kwargs):
        if self.get_argument('type') == '1':
            # 获取最新公告
            self.write(json.dumps(MainTool.get_notice(self.application.db)))
        elif self.get_argument('type') == '2':
            # 新增公告
            MainTool.add_notice(self.application.db, self.get_argument('content'))