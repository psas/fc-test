import socket
import config

class Comm(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', port))
        self.sock.settimeout(0.5)

    def send(self, port, message):
        print "Sending!!", port, message

        try:
            sock.sendto(message, (self.ip, port))
            data, remote_addr = sock.recvfrom(4096)
        except:
            data = None

        return data


RNH = {
    'comm': Comm(config.RNH_IP, 34000),
    'action-list': ["ARM", "Safe", "On1", "On2", "On3", "On4", "On6", "On7", "Off1", "Off2", "Off3", "Off4", "Off6", "Off7"],
    'actions': {
        'ARM': {'btn': "btn-danger",   'message': "#YOLO", 'port': config.RNH_LISTEN_PORT},
        'Safe': {'btn': "btn-success", 'message': "#SAFE", 'port': config.RNH_LISTEN_PORT},
        'On1': {'btn': "btn-default",  'message': "#ON_P"+chr(1<<1), 'port': config.RNH_LISTEN_PORT},
        'On2': {'btn': "btn-default",  'message': "#ON_P"+chr(1<<2), 'port': config.RNH_LISTEN_PORT},
        'On3': {'btn': "btn-default",  'message': "#ON_P"+chr(1<<3), 'port': config.RNH_LISTEN_PORT},
        'On4': {'btn': "btn-default",  'message': "#ON_P"+chr(1<<4), 'port': config.RNH_LISTEN_PORT},
        'On6': {'btn': "btn-default",  'message': "#ON_P"+chr(1<<6), 'port': config.RNH_LISTEN_PORT},
        'On7': {'btn': "btn-default",  'message': "#ON_P"+chr(1<<7), 'port': config.RNH_LISTEN_PORT},
        'Off1': {'btn': "btn-default",  'message': "#FF_P"+chr(1<<1), 'port': config.RNH_LISTEN_PORT},
        'Off2': {'btn': "btn-default",  'message': "#FF_P"+chr(1<<2), 'port': config.RNH_LISTEN_PORT},
        'Off3': {'btn': "btn-default",  'message': "#FF_P"+chr(1<<3), 'port': config.RNH_LISTEN_PORT},
        'Off4': {'btn': "btn-default",  'message': "#FF_P"+chr(1<<4), 'port': config.RNH_LISTEN_PORT},
        'Off6': {'btn': "btn-default",  'message': "#FF_P"+chr(1<<6), 'port': config.RNH_LISTEN_PORT},
        'Off7': {'btn': "btn-default",  'message': "#FF_P"+chr(1<<7), 'port': config.RNH_LISTEN_PORT},

    }
}
