# -*- coding: utf-8 -*-
import config
from base.checkparam import Param
from handler import root
from server.rsocket.gevent_socket import GeventSockect
from base.progress_handle import socket_deal

'''
server include master and slave, there is one master
slave need connect master, or shut down
any server has a root node, some user node
all root node use tcp connect other server
all node in the same server, connect by file socket
'''
class Ran():
    __setting = ''
    
    def __init__(self, setting):
        self.__setting = setting
        
    def status(self):
        #todo
        print ' print status'
        return
    
    def start(self):
        root_alive = root.alive()
        if self.__setting.node == 'root':
            if root_alive:
                print config.error('ROOT_RUNNING')
                return
            root.start()
        return
    
    def stop(self):
        #todo
        print 'stop haha'
        return
        
    def run(self):
        if self.__setting.option == 'status':
            self.status()
        if self.__setting.option == 'start':
            self.start()
        if self.__setting.option == 'stop':
            self.stop()
        if self.__setting.option == 'restart':
            self.stop()
            self.start()

def main():
    param = Param()
    setting = param.check()
    ran = Ran(setting)
    ran.run()