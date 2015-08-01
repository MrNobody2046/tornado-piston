import piston
import tornado.httpserver
import pony


class User(piston.Resource):
    def read(self):
        yield self.application.db.cursor("select * from test.user where id=%d" % self.req.user_id)


route = [
    ("/user", User),
]

settings = {
    "autoreload": True,

}


def server_forever():
    tornado.options.parse_command_line()
    application = tornado.web.Application(route, **settings)
    application.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    server_forever()
