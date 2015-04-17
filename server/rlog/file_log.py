# -*- coding: utf-8 -*-
import os

class FileLog():
    __log_path = ''
    __handle = None

    def __init__(self, log_path):
        self.__log_path = log_path
        log_folder = os.path.split(log_path)[0]
        if not os.path.exists(log_folder):
            raise IOError('folder does not exist!')
        if not os.path.exists(log_path):
            os.mknod(log_path) 

    def write(self, content):
        self.__handle = open(self.__log_path, 'a')
        self.__handle.write(content)
        self.__handle.close()
