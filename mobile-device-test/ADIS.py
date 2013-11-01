import threading
import socket
import struct
import time
import json
from random import gauss

RAD2DEG = 57.2957795
MSS2GEE = 1.0/9.81
ADIS_Header = struct.Struct('!4sHLH')
ADIS_Message = struct.Struct('<12H')
class SensorDevice(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.daemon = True

        self.queue = queue

        # Open socket and bind to address
        self.ADISsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ADISsocket.bind(('127.0.0.1', 35020))

    def ADISify_acc(self, acc):
        acc = json.loads(acc)
        x = acc['acc']['x']
        y = acc['acc']['y']
        z = acc['acc']['z']

        x = int((x*MSS2GEE)/0.00333)
        y = int((y*MSS2GEE)/0.00333)
        z = int((z*MSS2GEE)/0.00333)

        return x,y,z


    def mock_packet(self):
        p = [0]*12
        # Power
        p[0] = int(5.0/0.002418)
        # Gryo
        p[1] = int((gauss(0,0.1)*RAD2DEG)/0.05)
        p[2] = int((gauss(0,0.1)*RAD2DEG)/0.05)
        p[3] = int((gauss(0,0.1)*RAD2DEG)/0.05)
        # accel
        p[4] = 0
        p[5] = 0
        p[6] = 0
        # mag
        p[7] = 0
        p[8] = 0
        p[9] = 0
        # temp
        p[10] = int(24/0.14)
        # spare ADC
        p[11] = 0
        return p

    def run(self):
        while (not self._stop.is_set()):
            while not self.queue.empty():
                for x in self.queue.get():
                    v = self.mock_packet()
                    v[4], v[5], v[6] = self.ADISify_acc(x)

                    #twos' compliment
                    for i, n in enumerate(v):
                        if n<0:
                            n = (n-1 & 0xffff) + 1
                        v[i] = n

                    packet  = ADIS_Header.pack('ADIS', 0, 0, ADIS_Message.size)
                    packet += ADIS_Message.pack(*v)

                    self.ADISsocket.sendto(packet, ('127.0.0.1', 36000))
            time.sleep(0.01)

    def stop(self):
        self._stop.set()
        self.ADISsocket.close()
        self.join()


