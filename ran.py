# -*- coding: utf-8 -*-
from base.checkparam import Param
from handler.root import Root
from handler.user import User

class Ran():
    _setting = ''
    
    def __init__(self, setting):
        self._setting = setting
        
    def run(self):
        if self._setting.node == 'root':
            node = Root()
        else:
            node = User()
        node.set_param(self._setting.option, self._setting.task, self._setting.flag)
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