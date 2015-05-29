# -*- coding: utf-8 -*-
import config
from handler.node import Node
from lib.rsingleton import singleton
from lib.rthread import Rthread
import time
import sys

@singleton
class Root(Node):

    def _deal(self, option, task = '', flag = ''):
        if option == 'alive':
            return config.success()
        elif option == 'status':
            return config.success(self._status)
        elif option == 'start':
            return config.success()
        elif option == 'stop':
            config.running = False
            return config.success(self._status)
        
    def status(self):
        if not self._check():
            self._result = config.error('ROOT_NOT_RUNNING')
            return False
        result = self._send(option = 'status')
        if not result:
            self._result = config.error('ROOT_NOT_RUNNING')
            return False
        return result
    
    def start(self):
        if self._check() and self._send(option = 'alive'):
            self._result = config.error('ROOT_RUNNING')
            return False
        Rthread(self._listen, '_listen_root').start()
        return True
    
    def stop(self):
        if not self._check():
            self._result = config.error('ROOT_NOT_RUNNING')
            return False
        result = self._send(option = 'stop')
        if not result:
            self._result = config.error('ROOT_NOT_RUNNING')
            return False
        sys.stdout.write('Ran is stopping ')
        sys.stdout.flush()
        time.sleep(2)
        while True:
            result = self._send(option = 'stop')
            if not result:
                sys.stdout.write('ok')
                break
            elif result['running'] == False:
                sys.stdout.write('.')
            else:
                sys.stdout.write('stoping ')
            sys.stdout.flush()
            time.sleep(2)
        return False
    
    def run(self):
        self._socket = 'socket_root.d'
        if self._option == 'status':
            self.status()
            return False
        if self._option == 'start':
            self.start()
            return True
        if self._option == 'stop':
            self.stop()
            return False
