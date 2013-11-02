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

def action_Override_SLOCK():
    return SendToFC('DI_SLOCK', 35666)

def action_Enable_SLOCK():
    return SendToFC('EN_SLOCK', 35666)

def action_Enable_Servo():
    return SendToFC('ENABLE', 35667)

def action_Disable_Servo():
    return SendToFC('DISABLE', 35667)

def event_OpenLD():
    return SendToFC(chr(1), 35004)

def event_CloseLD():
    return SendToFC(chr(0), 35004)



actions = [
    {'action': "ARM", 'run': action_ARM},
    {'action': "SAFE", 'run': action_SAFE},
    {'action': "Override SLOCK", 'run': action_Override_SLOCK},
    {'action': "Enable SLOCK", 'run': action_Enable_SLOCK},
    {'action': "Enable Servo", 'run': action_Enable_Servo},
    {'action': "Disable Servo", 'run': action_Disable_Servo},
]

events = [
    {'action': "Simulate Launch Detect", 'run': event_OpenLD},
    {'action': "Simulate Launch Detect Reattach", 'run': event_CloseLD},
]
