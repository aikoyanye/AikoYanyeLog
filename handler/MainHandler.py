import tornado.web, json
from tool.main_tool import MainTool

class Mainhandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        # 如果cookie有用户数据，免登录
        email = self.get_cookie('email', '')
        username = self.get_cookie('username', '')
        userId = self.get_cookie('userId', '')
        if email != '' and username != '':
            self.render('body.html', current=True, user=(email, username), userId=userId)
        else:
            self.set_cookie('email', '')
            self.set_cookie('username', '')
            self.set_cookie('userId', '')
            self.render('body.html', current=False, userId=0)

    async def post(self, *args, **kwargs):
        if self.get_argument('hidden') == 'info':
            if MainTool.change_info(self.application.db, self.get_argument('info_email'), self.get_argument('info_username'),
                                    self.get_argument('info_oldpassword'), self.get_argument('info_password')):
                # 修改用户信息成功
                self.set_cookie('email', self.get_argument('info_email'))
                self.set_cookie('username', self.get_argument('info_username'))
                self.redirect('/')
            else:
                self.write('<script>alert("修改失败，注意字段")</script>')
        elif self.get_argument('hidden') == 'register':
            result = MainTool.register(self.application.db, self.get_argument('register_email'), self.get_argument('register_username'),
                                 self.get_argument('register_password'))
            if result:
                # 注册成功，将信息写入cookie
                self.set_cookie('email', result[0])
                self.set_cookie('username', result[1])
                self.set_cookie('userId', str(result[2]))
                self.redirect('/')
            else:
                self.write('<script>alert("注册失败，注意字段")</script>')
                self.redirect('/')

    async def delete(self, *args, **kwargs):
        # 注销
        self.set_cookie('email', '')
        self.set_cookie('username', '')
        self.set_cookie('userId', '')

    async def put(self, *args, **kwargs):
        if self.get_argument('hidden') == 'login':
            result = MainTool.login(self.application.db, self.get_argument('login_email'), self.get_argument('login_password'))
            if result:
                # 登录
                self.set_cookie('email', result[0])
                self.set_cookie('username', result[1])
                self.set_cookie('userId', str(result[2]))
                self.write('0')
            else:
                self.write(json.dumps(['1']))
