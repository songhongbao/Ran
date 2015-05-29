# -*- coding: utf-8 -*-
from base.checkparam import Param
from handler.root import Root
from handler.user import User

class Ran():
    __setting = ''
    
    def __init__(self, setting):
        self.__setting = setting
        
    def run(self):
        if self.__setting.node == 'root':
            node = Root()
        else:
            node = User()
        node.set_param(self.__setting.option, self.__setting.task, self.__setting.flag)
        result = node.run()
        if result == False:
            print node.result()
        else:
            print result

def main():
    param = Param()
    setting = param.check()
    ran = Ran(setting)
    ran.run()