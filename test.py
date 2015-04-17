#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

cur_path = os.path.split(os.path.realpath(__file__))[0]

sys.path.append(cur_path + '/server')

from server.rlog import rlog
from server.rsocket import tcpsocket

fsocket = tcpsocket.TcpSocket(7664)
fsocket.server()
while True:
    result = fsocket.receive()
    print result
    if result:
        fsocket.send('shoudaola')
    fsocket.close()
