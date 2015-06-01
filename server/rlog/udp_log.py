# -*- coding: utf-8 -*-
import socket

class UdpLog():
    _address = ('127.0.0.1', 5201)
    _handle = None

    def __init__(self, address):
        if address:
            self._address = address

    def write(self, content):
        if not self._handle:
            self._handle = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._handle.sendto(content, self._address)
