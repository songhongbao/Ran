# -*- coding: utf-8 -*-
from gevent.server import StreamServer

class GeventSockect():
    _host = ''
    _port = ''
    _func = ''
    
    def __init__(self, port):
        self._host = '0.0.0.0'
        self._port = port
        
    def deal(self, sock, address):
        fp = sock.makefile()
        while True:
            line = fp.readline().strip()
            if line:
                out = self._func(line)
                fp.write(out)
                fp.flush()
            else:
                break
        sock.close()
        
    
    def run(self, func):
        self._func = func
        server = StreamServer((self._host, self._port), self.deal)
        server.serve_forever()