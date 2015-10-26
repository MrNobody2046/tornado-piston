import piston
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
import tornado.gen
import tornado.httpclient
import urllib
import pony


class UserHandler(piston.BaseHandler):
    def read(self, user_id):
        print "RRRRR"
        query = "h"
        client = tornado.httpclient.AsyncHTTPClient()
        for _ in range(3):
            self.write("hhh%d\n" % _)
            r = yield tornado.gen.Task(client.fetch,
                                       "http://www.amazon.com")
            print r
        self.finish()
        # return {"hah": "user"}

    def post(self, *args, **kwargs):
        print self.request_obj

    print "FIni USERHandler"


class BookHandler(piston.BaseHandler):
    def read(self):
        self.write("haha")
        self.finish()


import asyncmongo
import tornado.web
#
#
# class Handler(tornado.web.RequestHandler):
#     @property
#     def db(self):
#         if not hasattr(self, '_db'):
#             self._db = asyncmongo.Client(pool_id='mydb', host='127.0.0.1', port=27017, maxcached=10, maxconnections=50,
#                                          dbname='test')
#         return self._db
#
#     @tornado.web.asynchronous
#     def get(self):
#         self.db.users.find({'username': self.current_user}, limit=1, callback=self._on_response)
#         # or
#         # conn = self.db.connection(collectionname="...", dbname="...")
#         # conn.find(..., callback=self._on_response)
#
#     def _on_response(self, response, error):
#         if error:
#             raise tornado.web.HTTPError(500)
#         self.render('template', full_name=response['full_name'])


route = [
    (r"/user/(\w+)", UserHandler.allow("GET")),
    (r"/book", BookHandler.allow("GET")),
]

settings = {
    "autoreload": True,
    "debug": True

}


def server_forever():
    tornado.options.parse_command_line()
    application = tornado.web.Application(route, **settings)
    application.listen(8111)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    server_forever()
