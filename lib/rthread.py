# -*- coding: utf-8 -*-
import threading

THREAD_FLAG = '*Rthread*'

class Rthread(threading.Thread):
    __func = ''
    __args = ''
    
    def __init__(self, func, name, *args):
        self.__func = func
        self.__args = args
        threading.Thread.__init__(self, group=None, target=None, name=THREAD_FLAG + name)
        return

    @staticmethod
    def AliveThread():
        alive_thread = []
        for cur_thread in threading.enumerate():
            if THREAD_FLAG in cur_thread.name:
                alive_thread.append(cur_thread.name[len(THREAD_FLAG) : ])
        return alive_thread

    @property
    def result(self):
        return self.__result

    def run(self):
        if len(self.__args) > 0:
            self.__func(*self.__args)
        else:
            self.__func()
        return True