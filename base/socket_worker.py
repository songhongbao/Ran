# -*- coding: utf-8 -*-
from gevent.server import StreamServer
import config

class SocketWorker():
    __host = ''
    __port = ''
    
    def __init__(self, port):
        self.__host = '0.0.0.0'
        self.__port = port
        
    def deal(self, sock, address):
        fp = sock.makefile()
        while True:
            line = fp.readline().strip()
            if line:
                print 1
                line += '\n'
                fp.write(line)
                fp.write(str(config.local_settings))
                fp.flush()
            else:
                break
        print 333
        sock.close()
        
    
    def run(self):
        server = StreamServer((self.__host, self.__port), self.deal)
        server.serve_forever()