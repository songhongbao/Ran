# -*- coding: utf-8 -*-
from gevent.server import StreamServer

class GeventSockect():
    __host = ''
    __port = ''
    __func = ''
    
    def __init__(self, port):
        self.__host = '0.0.0.0'
        self.__port = port
        
    def deal(self, sock, address):
        fp = sock.makefile()
        while True:
            line = fp.readline().strip()
            if line:
                out = self.__func(line)
                fp.write(out)
                fp.flush()
            else:
                break
        sock.close()
        
    
    def run(self, func):
        self.__func = func
        server = StreamServer((self.__host, self.__port), self.deal)
        server.serve_forever()