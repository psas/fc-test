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
        'ARM':  {'name': "ARM RNH",  'message': "#YOLO",           'from-port': 34000, 'btn': "danger"},
        'SAFE': {'name': "SAFE RNH", 'message': "#SAFE",           'from-port': 34000, 'btn': "safe"},
        'On1':  {'name': "1 On",     'message': "#ON_P"+chr(1<<1), 'from-port': 34000, 'btn': "warning"},
        'On2':  {'name': "2 On",     'message': "#ON_P"+chr(1<<2), 'from-port': 34000, 'btn': "warning"},
        'On3':  {'name': "3 On",     'message': "#ON_P"+chr(1<<3), 'from-port': 34000, 'btn': "warning"},
        'On4':  {'name': "4 On",     'message': "#ON_P"+chr(1<<4), 'from-port': 34000, 'btn': "warning"},
        'On6':  {'name': "6 On",     'message': "#ON_P"+chr(1<<6), 'from-port': 34000, 'btn': "warning"},
        'On7':  {'name': "7 On",     'message': "#ON_P"+chr(1<<7), 'from-port': 34000, 'btn': "warning"},
        'On8':  {'name': "8 On",     'message': "#ON_P"+chr(1<<5), 'from-port': 34000, 'btn': "warning"},
        'off1': {'name': "1 Off",    'message': "#FF_P"+chr(1<<1), 'from-port': 34000, 'btn': "default"},
        'off2': {'name': "2 Off",    'message': "#FF_P"+chr(1<<2), 'from-port': 34000, 'btn': "default"},
        'off3': {'name': "3 Off",    'message': "#FF_P"+chr(1<<3), 'from-port': 34000, 'btn': "default"},
        'off4': {'name': "4 Off",    'message': "#FF_P"+chr(1<<4), 'from-port': 34000, 'btn': "default"},
        'off6': {'name': "6 Off",    'message': "#FF_P"+chr(1<<6), 'from-port': 34000, 'btn': "default"},
        'off7': {'name': "7 Off",    'message': "#FF_P"+chr(1<<7), 'from-port': 34000, 'btn': "default"},
        'off8': {'name': "8 Off",    'message': "#FF_P"+chr(1<<5), 'from-port': 34000, 'btn': "default"},
    }
}

# Flight Computer Framework commands
FCF = {
    'comm': Comm(config.FC_IP, config.FC_LISTEN_PORT),
    'command-list': ["ARM", "SAFE", "disloc", "ensloc", "enservo", "diservo"],
    'commands': {
        'ARM':     {'name': "ARM FC",               'message': "#YOLO",     'from-port': config.FC_TALK_ARM, 'btn': "danger"},
        'SAFE':    {'name': "SAFE FC",              'message': "#SAFE",     'from-port': config.FC_TALK_ARM, 'btn': "safe"},
        'disloc':  {'name': "Override Sensor Lock", 'message': "DI_SLOCK",  'from-port': config.FC_TALK_ARM, 'btn': "warning"},
        'ensloc':  {'name': "Enable Sensor Lock",   'message': "EN_SLOCK",  'from-port': config.FC_TALK_ARM, 'btn': "default"},
        'enservo': {'name': "Enable Roll Servo",    'message': "ENABLE",    'from-port': config.FC_TALK_SERVO, 'btn': "warning"},
        'diservo': {'name': "Disable Roll Servo",   'message': "DISABLE",   'from-port': config.FC_TALK_SERVO, 'btn': "default"},
    }
}
