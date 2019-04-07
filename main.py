import tornado.web, tornado.ioloop, tornado.locks, sqlite3, os
from handler.MainHandler import Mainhandler
from handler.TitleHandler import TitleHandler
from handler.ContentHandler import ContentHandler

class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        handlers = [
            tornado.web.url(r'/', Mainhandler, name='main'),
            tornado.web.url(r'/title', TitleHandler, name='title'),
            tornado.web.url(r'/content', ContentHandler, name='content'),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True,
            xsrf_cookie=True,
        )
        super(Application, self).__init__(handlers, **settings)

async def main():
    db = sqlite3.connect('log.db')
    app = Application(db)
    app.listen(8080)
    await tornado.locks.Event().wait()

if __name__ == '__main__':
    tornado.ioloop.IOLoop.current().run_sync(main)