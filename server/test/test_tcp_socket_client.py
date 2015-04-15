# -*- coding: utf-8 -*-
import sys
import os

cur_path = os.path.split(os.path.realpath(__file__))[0]

sys.path.append(cur_path + '/../server')

from log import rlog
from rsocket import tcpsocket

socket = tcpsocket.TcpSocket(7664)
socket.server()
while True:
    result = socket.receive()
    print result
    if result:
        socket.send('shoudaola')
    socket.close()
