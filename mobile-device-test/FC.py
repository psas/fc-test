import socket

FC_IP = '127.0.0.1'
FC_LISTEN_PORT = 36000

def SendToFC(message, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    sock.settimeout(0.1)

    try:
        sock.sendto(message, (FC_IP, FC_LISTEN_PORT))
        data, remote_addr = sock.recvfrom(4096)
    except:
        data = None

    sock.close()

    return data

def action_ARM():
    return SendToFC('#YOLO', 35666)
def action_SAFE():
    return SendToFC('#SAFE', 35666)
def action_Disable_Servo():
    return SendToFC('DISABLE', 35667)


actions = [
        {'action': "ARM", 'run': action_ARM},
        {'action': "SAFE", 'run': action_SAFE},
        {'action': "Override SLOCK"},
        {'action': "Enable Servo"},
        {'action': "Disable Servo", 'run': action_Disable_Servo},
]
