#!/usr/bin/env sh
sudo socat PTY,user=$USERNAME,link=/tmp/USBGPSTESTDEVICE PTY,user=$USERNAME,link=/dev/ttyS11
