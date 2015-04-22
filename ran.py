# -*- coding: utf-8 -*-
import config
from base.checkparam import Param
#from base.socket_worker import SocketWorker
from server.rsocket.geventSocket import GeventSockect
from base.progress_handle import socket_deal

def ran_user():
    pass

def ran_root():
    #to do
    #check root exist
    worker = GeventSockect(config.config('socket_port'))
    worker.run(socket_deal)

def ran_child():
    pass



def run():
    param = Param()
    setting = param.check()
    if setting.node == 'root':
        ran_root()