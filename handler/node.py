# -*- coding: utf-8 -*-
import config
from lib.rthread import Rthread
from lib.rsingleton import singleton
import json
import os
from server.rsocket.file_socket import FileSocket

class Node():
    _option = ''
    _task = ''
    _flag = 0
    _status = {'status' : 'green', 'list' : [], 'running' : True}
    _result = 'result is empty'
    _socket = ''
    
    def set_param(self, option, task, flag):
        if option:
            self._option = option
        if task:
            self._task = task
        if flag:
            self._flag = flag
            
    def result(self):
        return self._result
        
    def _deal(self, option, task = '', flag = ''):
        pass
        
    def _listen(self):
        #delete socket file
        if self._check():
            self._delete()
        #init root socket
        socket_file = config.config('socket_folder') + '/' + self._socket
        fsocket = FileSocket(socket_file)
        fsocket.server()
        while True:
            data = fsocket.receive()
            if not data:
                continue
            try:
                param = json.loads(data)
            except Exception, e:
                param = False
            if not param:
                result = config.error('NOT_JSON', data)
            elif not isinstance(param, dict):
                result = config.error('PARAM_ILLEGAL', data)
            elif not param.get('option'):
                result = config.error('MISSING_VALUE', 'Option key error.')
            else:
                result = self._deal(param.get('option'), param.get('task'), param.get('flag'))
            fsocket.send(result)
            fsocket.close()
            #check stop
            if config.running == False:
                self._status['running'] = False
                break
        
    def _check(self):
        socket_file = config.config('socket_folder') + '/' + self._socket
        return os.path.exists(socket_file)
    
    def _delete(self):
        socket_file = config.config('socket_folder') + '/' + self._socket
        os.unlink(socket_file)
        
    def _send(self, option = '', task = '', flag = ''):
        if self._check() == False:
            return False
        param = dict()
        param['option'] = option
        param['task'] = task
        param['flag'] = flag
        data = json.dumps(param)
        socket_file = config.config('socket_folder') + '/' + self._socket
        try:
            fsocket = FileSocket(socket_file)
            fsocket.client()
            fsocket.send(data)
            recieve = fsocket.receive()
            result = json.loads(recieve)
            fsocket.close()
        except Exception, e:
            #socket file exist, but can not connect
            result = False
        finally:
            return result
        
    def start(self):
        pass
    
    def stop(self):
        pass
    
    def status(self):
        pass
            
        
