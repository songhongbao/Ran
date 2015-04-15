# -*- coding: utf-8 -*-
import socket
import time
import os
from log import rlog

R_SERVER = 'server'
R_CLIENT = 'client'

class TcpSocket():
    __tcp_address = ''
    __type = ''
    __server_socket = None
    __client_socket = None
    
    def __init__(self, tcp_port):
        self.__tcp_address = ('0.0.0.0', tcp_port)
    
    def server(self):
        self.__type = R_SERVER
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.__server_socket.setblocking(0)
        #SO_REUSEADDR fix socket.error: Address already in use
        self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print self.__tcp_address
        self.__server_socket.bind(self.__tcp_address)
        self.__server_socket.listen(5)
        self.__server_socket.settimeout(60)
        
    def client(self):
        self.__type = R_CLIENT
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.connect(self.__tcp_address)
        
    def receive(self):
        start_time = time.time()
        is_success = True
        result = ''
        try:
            if self.__type == R_SERVER:
                self.__client_socket = self.__server_socket.accept()[0]
                result = self.__client_socket.recv(1024)
            else:
                result = self.__server_socket.recv(1024)
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
                rlog.write( self.__tcp_address[0] + ':' + str(self.__tcp_address[1]), 
                            rlog.LOG_TYPE_FSOCKET, 
                            time.time() - start_time,
                            self.__type + ' receive', 
                            result, 
                            is_success)
                
    def send(self, msg):
        if msg == '':
            return
        start_time = time.time()
        is_success = True
        result = ''
        try:
            if self.__type == R_SERVER:
                self.__client_socket.send(msg)
            else:
                self.__server_socket.send(msg)
            result = msg
            return True
        except Exception, e:
            result = e
            is_success = False
            return False
        finally:
            if result != '':
                result = str(result)
                rlog.write( self.__tcp_address[0] + ':' + str(self.__tcp_address[1]),
                            rlog.LOG_TYPE_FSOCKET, 
                            time.time() - start_time,
                            self.__type + ' send', 
                            str(result), 
                            is_success)
        
    def close(self):
        if self.__type == R_SERVER and self.__client_socket:
            self.__client_socket.close()
            self.__client_socket = None
        if self.__type == R_CLIENT and self.__server_socket:
            self.__server_socket.close()
            self.__server_socket = None