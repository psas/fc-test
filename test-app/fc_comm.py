import socket
import config

def SendToFC(message, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    sock.settimeout(0.1)

    try:
        sock.sendto(message, (config.FC_IP, config.FC_LISTEN_PORT))
        data, remote_addr = sock.recvfrom(4096)
    except:
        data = None

    sock.close()

    return data

# Define actions:
def action_ARM():
    return SendToFC('#YOLO', config.FC_TALK_ARM)

def action_SAFE():
    return SendToFC('#SAFE', config.FC_TALK_ARM)

def action_Override_SLOCK():
    return SendToFC('DI_SLOCK', config.FC_TALK_ARM)

def action_Enable_SLOCK():
    return SendToFC('EN_SLOCK', config.FC_TALK_ARM)

def action_Enable_Servo():
    return SendToFC('ENABLE', config.FC_TALK_SERVO)

def action_Disable_Servo():
    return SendToFC('DISABLE', config.FC_TALK_SERVO)

def event_OpenLD():
    return SendToFC(chr(1), config.ROLL_TX_PORT)

def event_CloseLD():
    return SendToFC(chr(0), config.ROLL_TX_PORT)


actions = [
    {'action': "ARM", 'btn': "btn-danger", 'run': action_ARM},
    {'action': "SAFE", 'btn': "btn-success", 'run': action_SAFE},
    {'action': "Override SLOCK", 'btn': "btn-warning", 'run': action_Override_SLOCK},
    {'action': "Enable SLOCK", 'btn': "btn-default", 'run': action_Enable_SLOCK},
    {'action': "Enable Servo", 'btn': "btn-warning", 'run': action_Enable_Servo},
    {'action': "Disable Servo", 'btn': "btn-default", 'run': action_Disable_Servo},
]

events = [
    {'action': "Launch Detect", 'btn': "btn-danger",'run': event_OpenLD},
    {'action': "Launch Detect Reattach", 'btn': "btn-default",'run': event_CloseLD},
]
