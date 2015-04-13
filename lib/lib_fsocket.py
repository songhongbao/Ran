# -*- coding: utf-8 -*-
#!/usr/bin/python

import socket
import time
import loglib
import os

class RanFsocket():
    def __init__(self, file_handle, flag = 'server'):
        self.__file_handle = file_handle
        self.__flag = flag
        self.__server_socket = ''
        self.__client_socket = ''
        self.__client_addr = ''
        
    def listen(self):
        self.__server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        #self.__server_socket.setblocking(0)
        #SO_REUSEADDR fix socket.error: Address already in use
        if self.__flag == 'server':
            self.__server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if os.path.exists(self.__file_handle):  
                os.unlink(self.__file_handle)
            self.__server_socket.bind(self.__file_handle)
            self.__server_socket.listen(5)
            self.__server_socket.settimeout(60)
        else:
            self.__server_socket.connect(self.__file_handle)
        
    def receive(self):
        start_time = time.time()
        _result = ''
        _is_success = True
        try:
            if self.__flag == 'server':
                self.__client_socket, self.__client_addr = self.__server_socket.accept()
                _result = self.__client_socket.recv(1024)
                _is_success = True
            else:
                _result = self.__server_socket.recv(1024)
                _is_success = True
            return _result
        except socket.timeout:
            return True
        except Exception, e:
            _result = e
            _is_success = False
            return False
        finally:
            if _result != '':
                rlog = loglib.SimpleLog()
                rlog.log(   'localhost:80',
                            'socket',
                            time.time() - start_time,
                            str(self.__file_handle.split('/')[-1]),
                            self.__flag + ' Receive : ' + str(_result),
                            _is_success)
                
    def send(self, msg):
        start_time = time.time()
        _result = ''
        _is_success = True
        try:
            if self.__flag == 'server':
                self.__client_socket.send(msg)
            else:
                self.__server_socket.send(msg)
            _result = msg
            _is_success = True
            return True
        except socket.timeout:
            return True
        except Exception, e:
            _result = e
            _is_success = False
            return False
        finally:
            if _result != '':
                rlog = loglib.SimpleLog()
                rlog.log(   'localhost:80',
                            'socket',
                            time.time() - start_time,
                            str(self.__file_handle.split('/')[-1]),
                            self.__flag + ' Send : ' + str(_result),
                            _is_success)
        
    def close(self):
        if self.__flag == 'server' and self.__client_socket:
            self.__client_socket.close()
        if self.__flag == 'client' and self.__server_socket:
            self.__server_socket.close()