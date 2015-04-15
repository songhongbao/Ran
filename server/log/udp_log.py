# -*- coding: utf-8 -*-
import socket

class UdpLog():
    __address = ('127.0.0.1', 5201)
    __handle = None

    def __init__(self, address):
        if address:
            self.__address = address

    def write(self, content):
        if not self.__handle:
            self.__handle = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__handle.sendto(content, self.__address)
