#!/usr/bin/env python
import tornado.web
import tornado.websocket
import tornado.ioloop
import ADIS
import os

static_path = os.path.join(os.path.dirname(__file__), 'static')
template_path = os.path.join(os.path.dirname(__file__), 'templates')

# Fake ADIS device
adis = ADIS.SensorDevice()

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class FrontEndWebSocket(tornado.websocket.WebSocketHandler):

    clients = []

    def open(self):
        if self not in self.clients:
            self.clients.append(self)

    def on_message(self, message):
        adis.send_message(message)

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

    # Start
    tornado.ioloop.IOLoop.instance().start()

