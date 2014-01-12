import socket
import config

class Comm(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', port))
        #self.sock.settimeout(0.5)

    def send(self, port, message):
        print "Sending!!", port, message

        data = self.sock.sendto(message, (self.ip, port))

        """
        try:
            sock.sendto(message, (self.ip, port))
            data, remote_addr = sock.recvfrom(4096)
            print data
        except:
            data = None
        """

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
