# -*- coding: utf-8 -*-
import socket
import time
from server.rlog import rlog

R_SERVER = 'server'
R_CLIENT = 'client'

class TcpSocket():
    _tcp_address = ''
    _type = ''
    _server_socket = None
    _client_socket = None
    
    def __init__(self, tcp_port):
        self._tcp_address = ('0.0.0.0', tcp_port)
    
    def server(self):
        self._type = R_SERVER
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self._server_socket.setblocking(0)
        #SO_REUSEADDR fix socket.error: Address already in use
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print self._tcp_address
        self._server_socket.bind(self._tcp_address)
        self._server_socket.listen(5)
        self._server_socket.settimeout(60)
        
    def client(self):
        self._type = R_CLIENT
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.connect(self._tcp_address)
        
    def receive(self):
        start_time = time.time()
        is_success = True
        result = ''
        try:
            if self._type == R_SERVER:
                self._client_socket = self._server_socket.accept()[0]
                result = self._client_socket.recv(1024)
            else:
                result = self._server_socket.recv(1024)
            return result
        except socket.timeout:
            return result
        except Exception, e:
            result = e
            is_success = False
            return False
        finally:
            if result != '':
                result = str(result)
                rlog.write( self._tcp_address[0] + ':' + str(self._tcp_address[1]), 
                            rlog.LOG_TYPE_FSOCKET, 
                            time.time() - start_time,
                            self._type + ' receive', 
                            result, 
                            is_success)
                
    def send(self, msg):
        if msg == '':
            return
        start_time = time.time()
        is_success = True
        result = ''
        try:
            if self._type == R_SERVER:
                self._client_socket.send(msg)
            else:
                self._server_socket.send(msg)
            result = msg
            return True
        except Exception, e:
            result = e
            is_success = False
            return False
        finally:
            if result != '':
                result = str(result)
                rlog.write( self._tcp_address[0] + ':' + str(self._tcp_address[1]),
                            rlog.LOG_TYPE_FSOCKET, 
                            time.time() - start_time,
                            self._type + ' send', 
                            str(result), 
                            is_success)
        
    def close(self):
        if self._type == R_SERVER and self._client_socket:
            self._client_socket.close()
            self._client_socket = None
        if self._type == R_CLIENT and self._server_socket:
            self._server_socket.close()
            self._server_socket = None