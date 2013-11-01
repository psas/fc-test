#!/usr/bin/env python
import tornado.web
import tornado.websocket
import tornado.ioloop
import ADIS
import Queue
import os

static_path = os.path.join(os.path.dirname(__file__), 'static')
template_path = os.path.join(os.path.dirname(__file__), 'templates')

# queue for placing messages upstream
q = Queue.Queue()

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class FrontEndWebSocket(tornado.websocket.WebSocketHandler):

    clients = []

    def open(self):
        if self not in self.clients:
            self.clients.append(self)

    def on_message(self, message):
        q.put([message])

    def on_close(self):
        if self in self.clients:
            self.clients.remove(self)


if __name__ == "__main__":

    # setup
    application = tornado.web.Application([
            (r'/', MainHandler),
            (r'/ws', FrontEndWebSocket),
            (r'/(.*)', tornado.web.StaticFileHandler, dict(path=static_path)),
        ], template_path=template_path, static_path=static_path)
    application.listen(5000)

    # Fake ADIS device
    adis = ADIS.SensorDevice(q)

    # threads
    try:
        adis.start()
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt, SystemExit:
        adis.stop()
