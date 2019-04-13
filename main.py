import tornado.web, tornado.ioloop, tornado.locks, sqlite3, os
from handler.MainHandler import MainHandler, UpdateHandler
from handler.TitleHandler import TitleHandler
from handler.ContentHandler import ContentHandler
from handler.CommentHandler import CommentHandler
from handler.PanHandler import PanHandler
from handler.SearchHandler import SearchHandler

class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        handlers = [
            tornado.web.url(r'/', MainHandler, name='main'),
            tornado.web.url(r'/title', TitleHandler, name='title'),
            tornado.web.url(r'/content', ContentHandler, name='content'),
            tornado.web.url(r'/comment', CommentHandler, name='comment'),
            tornado.web.url(r'/pan', PanHandler, name='pan'),
            tornado.web.url(r'/update', UpdateHandler, name='update'),
            tornado.web.url(r'/search', SearchHandler, name='search'),
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
    app.listen(port=8080)
    await tornado.locks.Event().wait()

if __name__ == '__main__':
    tornado.ioloop.IOLoop.current().run_sync(main)