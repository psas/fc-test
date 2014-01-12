import socket
import config

class Comm(object):

    def __init__(self, to_ip, to_port):
        """to_ip is the address sockets will send to, same with port"""
        self.ip = to_ip
        self.port = to_port

    def send(self, port, message):
        """port is the port the message should come from, and message is what is sent"""

        # Debug
        print "Sending!!", port, message

        # Build socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', port))
        data = sock.sendto(message, (self.ip, self.port))

        return data


# Rocket Net Hub commands
RNH = {
    'comm': Comm(config.RNH_IP, config.RNH_LISTEN_PORT),
    'command-list': ["ARM", "SAFE"],
    'commands': {
        'ARM':  {'name': "ARM RNH",  'message': "#YOLO", 'from-port': 34000, 'btn': "danger"},
        'SAFE': {'name': "SAFE RNH", 'message': "#SAFE", 'from-port': 34000, 'btn': "safe"},

        'On1':  {'name': "IMU On", 'btn': "btn-warning",  'message': "#ON_P"+chr(1<<1), 'port': config.RNH_LISTEN_PORT},
        'On2':  {'name': "2 On", 'btn': "btn-warning",  'message': "#ON_P"+chr(1<<2), 'port': config.RNH_LISTEN_PORT},
        'On3':  {'name': "3 On", 'btn': "btn-warning",  'message': "#ON_P"+chr(1<<3), 'port': config.RNH_LISTEN_PORT},
        'On4':  {'name': "FC On", 'btn': "btn-warning",  'message': "#ON_P"+chr(1<<4), 'port': config.RNH_LISTEN_PORT},
        'On6':  {'name': "6 On", 'btn': "btn-warning",  'message': "#ON_P"+chr(1<<6), 'port': config.RNH_LISTEN_PORT},
        'On7':  {'name': "7 On", 'btn': "btn-warning",  'message': "#ON_P"+chr(1<<7), 'port': config.RNH_LISTEN_PORT},
        'Off1': {'name': "IMU Off", 'btn': "btn-default",  'message': "#FF_P"+chr(1<<1), 'port': config.RNH_LISTEN_PORT},
        'Off2': {'name': "2 Off", 'btn': "btn-default",  'message': "#FF_P"+chr(1<<2), 'port': config.RNH_LISTEN_PORT},
        'Off3': {'name': "3 Off", 'btn': "btn-default",  'message': "#FF_P"+chr(1<<3), 'port': config.RNH_LISTEN_PORT},
        'Off4': {'name': "FC Off", 'btn': "btn-default",  'message': "#FF_P"+chr(1<<4), 'port': config.RNH_LISTEN_PORT},
        'Off6': {'name': "6 Off", 'btn': "btn-default",  'message': "#FF_P"+chr(1<<6), 'port': config.RNH_LISTEN_PORT},
        'Off7': {'name': "7 Off", 'btn': "btn-default",  'message': "#FF_P"+chr(1<<7), 'port': config.RNH_LISTEN_PORT},

    }
}

# Flight Computer Framework commands
FCF = {
    'comm': Comm(config.FC_IP, config.FC_LISTEN_PORT),
    'command-list': ["ARM", "SAFE"],
    'commands': {
        'ARM':  {'name': "ARM FC",  'message': "#YOLO", 'from-port': config.FC_TALK_ARM, 'btn': "danger"},
        'SAFE': {'name': "SAFE FC", 'message': "#SAFE", 'from-port': config.FC_TALK_ARM, 'btn': "safe"},
    }
}
