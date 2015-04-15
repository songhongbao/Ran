#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import time

cur_path = os.path.split(os.path.realpath(__file__))[0]

sys.path.append(cur_path + '/server')

from log import rlog
from rsocket import tcpsocket

while True:
    fsocket = tcpsocket.TcpSocket(7664)
    fsocket.client()
    fsocket.send('statusgyhoup8pyoiyodsdsdsdgf')
    data = fsocket.receive()
    fsocket.close()
    time.sleep(1)
