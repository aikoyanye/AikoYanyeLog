import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    async def prepare(self):
        cursor = self.application.db.cursor()
        ip = str(self.request.remote_ip)
        p_ip = '.'.join(ip.split('.')[:2])
        sql = 'SELECT id FROM ban_ip WHERE ip = "{}" OR ip = "{}"'.format(ip, p_ip)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        print(result)
        if result is not None:
            self.render('404.html')
            return