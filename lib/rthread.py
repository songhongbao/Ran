# -*- coding: utf-8 -*-
import threading

THREAD_FLAG = '*Rthread*'

class Rthread(threading.Thread):
    _func = ''
    _args = ''
    
    def __init__(self, func, name, *args):
        self._func = func
        self._args = args
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
        return self._result

    def run(self):
        if len(self._args) > 0:
            self._func(*self._args)
        else:
            self._func()
        return True