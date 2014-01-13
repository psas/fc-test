#!/usr/bin/env python
import tornado.web
import tornado.websocket
import tornado.ioloop
import e407_sensor as ADIS
import fc_comm as FC
import comm
import os
import datetime
import config

static_path = os.path.join(os.path.dirname(__file__), 'static')
template_path = os.path.join(os.path.dirname(__file__), 'templates')

# Fake ADIS device
adis = ADIS.SensorDevice()

event_log = []

# periodic callback for sending random data
sched = tornado.ioloop.PeriodicCallback(adis.send_random, 10)


class TestState(object):
    """FSM for running the test framework app"""

    # State Enumus
    ADIS_TRANS   = 0b0001
    ADIS_MOBILE  = 0b0010

    def __init__(self):
        # Default state
        self.state = 0

    # Events:
    def connect(self):
        self.state ^= TestState.ADIS_TRANS

    def radio(self):
        self.state ^= TestState.ADIS_MOBILE

state = TestState()

# index page
class MainHandler(tornado.web.RequestHandler):
    def get(self):

        connected = False
        if (state.state & TestState.ADIS_TRANS) > 0:
            connected = True
            sched.start()
        else:
            sched.stop()


        self.render('index.html', actions=FC.actions, events=FC.events, log=event_log, conn=connected)

    def post(self):
        abtn = self.get_argument('action', None)
        ebtn = self.get_argument('event', None)
        conbtn = self.get_argument('connectsensor', None)

        if conbtn is not None:
            state.connect()

        connected = False
        if (state.state & TestState.ADIS_TRANS) > 0:
            connected = True
            sched.start()
        else:
            sched.stop()

        if abtn is not None:
            action = FC.actions[int(abtn)].get('run')
            if action is not None:
                message = action()
                t = datetime.datetime.now().strftime('%H:%M:%S')
                event_log.append((t, FC.actions[int(abtn)].get('action'), message))

        if ebtn is not None:
            action = FC.events[int(ebtn)].get('run')
            if action is not None:
                message = action()
                t = datetime.datetime.now().strftime('%H:%M:%S')
                event_log.append((t, FC.events[int(ebtn)].get('action'), message))

        self.render('index.html', actions=FC.actions, events=FC.events, log=event_log, conn=connected)\


# Direct FC page

class FCHandler(tornado.web.RequestHandler):

    sections = [
        {'name': "RNH Commands", 'type': "RNH", 'def': comm.RNH},
        {'name': "FC Commands",  'type': "FCF", 'def': comm.FCF}
    ]

    def get(self, command):
        if command == '':
            self.render('fc-stack.html', sections=self.sections)
        else:
            print command
            module, command = command.split('/')
            for s in self.sections:
                if module == s['type']:
                    command = s['def']['commands'][command]
                    message = command['message']
                    port = command['from-port']
                    s['def']['comm'].send(port, message)
            self.redirect('/fc-stack/')


# mobile page
class MobileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('mobile.html')


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
            (r'/fc/(.*)', FCHandler),
            (r'/mobile', MobileHandler),
            (r'/ws', FrontEndWebSocket)
        ], template_path=template_path, static_path=static_path)
    application.listen(config.WEBSERVICE_PORT)

    # Start
    tornado.ioloop.IOLoop.instance().start()

