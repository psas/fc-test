#!/usr/bin/env python
import socket
import pynmea2
import serial
import struct



TCP_IP = '127.0.0.1'
TCP_PORT = 50000
BUFFER_SIZE = 12000

DEVICE = '/dev/ttyS11'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


ser = serial.Serial(DEVICE, 115200, timeout=0.1)

BIN1 = struct.Struct('<4sHHBBHdddfffffHHH2s')


#s.send(MESSAGE)

while True:
    data = s.recv(BUFFER_SIZE)
    #print "Raw data: ", data

    for line in data.split('\n'):
        
        # Read message in
        try:
            msg = pynmea2.parse(line)
        except:
            print "parse fail", line
            msg = None
        if msg:
            if msg.type == "GGA":
                print "Got GGA", msg.num_sats, msg.lat, msg.lon, msg.altitude

                packet = BIN1.pack('$BIN',
                    1,                      # type
                    52,                     # data len
                    0,                      # age
                    int(msg.num_sats),
                    0,                      # week
                    0,                      # time
                    float(msg.latitude),
                    float(msg.longitude),
                    0,
                    0,                      # V N
                    0,                      # V E
                    0,                      # V U
                    0,                      # Std Dev residual
                    1<<2,                   # Nav mode
                    0,                      # age of diff
                    0,                      # checksim
                    '\r\n'
                )

                chksm = 0
                for byte in packet[8:-4]:
                    chksm += ord(byte)
                
                print chksm
                packet = BIN1.pack('$BIN',
                    1,                      # type
                    52,                     # data len
                    0,                      # age
                    int(msg.num_sats),
                    0,                      # week
                    0,                      # time
                    float(msg.latitude),
                    float(msg.longitude),
                    0,
                    0,                      # V N
                    0,                      # V E
                    0,                      # V U
                    0,                      # Std Dev residual
                    1<<2,                   # Nav mode
                    0,                      # age of diff
                    chksm,                  # checksim
                    '\r\n'
                )

                ser.write(packet)

            """
            for field in msg.fields:
                print field
            #print msg.type, msg.fields
            """
        """
        try:
        except: 
            #print "failed!: ", line
            pass
        """

s.close()
