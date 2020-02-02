import tornado
import tornado.web


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('<script>location.href="/dashboard";</script>')


class KillHandler(tornado.web.RequestHandler):

    def get(self):
        tornado.ioloop.IOLoop().add_callback(tornado.ioloop.IOLoop().stop)
        tornado.ioloop.IOLoop().current().stop()
