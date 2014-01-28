#!/usr/bin/env python
import socket
import pynmea2

TCP_IP = '127.0.0.1'
TCP_PORT = 50000
BUFFER_SIZE = 12000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

#s.send(MESSAGE)

while True:
    data = s.recv(BUFFER_SIZE)
    #print "Raw data: ", data

    for line in data.split('\n'):
        try:
            # Read message in
            msg = pynmea2.parse(line)
            print "Parsed: ", msg, "Type:", msg.type

            if msg.type == "GGA":
                print "------------------"
                print "Qual:", msg.gps_qual, "Num sats", msg.num_sats, "HDOP:", msg.horizontal_dil, "Alt:", msg.altitude
            """
            for field in msg.fields:
                print field
            #print msg.type, msg.fields
            """
        except: 
            #print "failed!: ", line
            pass

s.close()


