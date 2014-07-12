#!/usr/bin/env python

from contextlib import closing
import itertools
import math
import os
from psas_packet import network, messages
import socket
import struct
import sys
from threading import Thread
import time

data_dir = sys.argv[1]

# original data. See: <https://github.com/psas/Launch-11>
rolldata_file = os.path.join(data_dir, 'rollcontrol/resampled_roll_data.csv')

# constants
dt = 1 / 819.2
servo_struct = struct.Struct(">IHB")

PWM_TICKS_MAX = 56000
PWM_US_MAX = 3333
MAX_SERVO_POSITION_US = 1900.0
MIN_SERVO_POSITION_US = 1100.0
MAX_SERVO_POSITION_TICKS = MAX_SERVO_POSITION_US * PWM_TICKS_MAX / PWM_US_MAX
MIN_SERVO_POSITION_TICKS = MIN_SERVO_POSITION_US * PWM_TICKS_MAX / PWM_US_MAX
MAX_CANARD_ANGLE = 15.0
MIN_CANARD_ANGLE = -15.0
CANARD_PWM_TICKS_PER_DEGREE = (MAX_SERVO_POSITION_TICKS - MIN_SERVO_POSITION_TICKS) / (MAX_CANARD_ANGLE - MIN_CANARD_ANGLE)
CANARD_PWM_TICKS_CENTER = MIN_SERVO_POSITION_TICKS - CANARD_PWM_TICKS_PER_DEGREE * MIN_CANARD_ANGLE

LOCALHOST = '127.0.0.1'
ROLL_RX_PORT    = 35003
ADIS_TX_PORT    = 35020
FC_TALK_SERVO   = 35667
FC_LISTEN_PORT  = 36000

def call(f): return f()
@call
def roll_coefficient():
    rho = 1.225 # assume constant sea-level air density because I'm lazy
    I = 0.0055747854 + 0.0113514922 / 2 # assume constantly half-full of fuel because see above
    F = 4 # number of canards
    r = 0.082 # m, distance of canard center of pressure from center axis
    A = 0.001164 # m^2, canard area
    magic = 2000 # I dunno, the real thing doesn't behave like the model
    return F * A * r * 0.5 * rho / I / magic

# global state
seq = 0
velocity = 0.0
fin_angle = 0.0
roll_rate = 0.0

def update_roll_rate():
    global roll_rate

    K_P = 2.45
    K_V = 3.21
    fin_cos = math.cos(fin_angle)
    fin_sin = math.sin(fin_angle)
    C_L = K_P * fin_cos ** 2 * fin_sin + K_V * fin_cos * fin_sin ** 2

    roll_accel = roll_coefficient * C_L * (velocity ** 2)
    roll_rate += roll_accel * dt

def sender():
    with open(rolldata_file) as accel_file:
        accel = itertools.imap(lambda line: float(line.split(',', 1)[0]), accel_file)
        with network.SendUDP(LOCALHOST, FC_LISTEN_PORT, from_port=ADIS_TX_PORT) as adis:
            velocity = 0.0
            for seq, accel_sample in enumerate(accel):
                start = time.time()

                adis.send_seq_message(messages.ADIS, seq, {
                    'Acc_X': accel_sample,
                    'Gyro_X': roll_rate * 180 / math.pi,
                })

                velocity += accel_sample * dt
                update_roll_rate()

                wait_time = dt - (time.time() - start)
                if wait_time > 0:
                    time.sleep(wait_time)
    sys.exit(0)

Thread(target=sender).start()

with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
    sock.bind((LOCALHOST, FC_TALK_SERVO))
    sock.sendto('ENABLE', (LOCALHOST, FC_LISTEN_PORT))

servo_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servo_socket.bind((LOCALHOST, ROLL_RX_PORT))
for pkt in iter(lambda: servo_socket.recv(1500), None):
    seq, cmd, enable = servo_struct.unpack(pkt)
    new_angle = 0.0
    if enable:
        new_angle = (cmd - CANARD_PWM_CENTER) / CANARD_PWM_PER_DEGREE

    if new_angle > MAX_CANARD_ANGLE:
        new_angle = MAX_CANARD_ANGLE
    if new_angle < MIN_CANARD_ANGLE:
        new_angle = MIN_CANARD_ANGLE

    fin_angle = new_angle
