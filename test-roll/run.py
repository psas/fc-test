#!/usr/bin/env python
import csv
import os
from psas_packet import messages, network
import sys
import time

data_dir = sys.argv[1]

# original data. See: <https://github.com/psas/Launch-11>
rolldata_file = os.path.join(data_dir, 'rollcontrol/resampled_roll_data.csv')

accel = []
roll = []
with open(rolldata_file) as f:
    for line in csv.reader(f):
        accel.append(float(line[0]))
        roll.append(float(line[1]))

adis_sample_rate = 819.2   # Hz

now = time.time()
last_pack_sent = 0

for i, a in enumerate(accel):
    with network.SendUDP('127.0.0.1', 36000, from_port=35020) as udp:
        data = {
            'Acc_X': a,
            'Gyro_X': roll[i] * 57.29577 # radians to degrees
        }
        now = time.time()
        real_delay = now - last_pack_sent
        wait_time = (1/adis_sample_rate) - real_delay
        if wait_time > 0:
            time.sleep(wait_time)
        udp.send_seq_data(messages.ADIS, i, data)
        last_pack_sent = time.time()
