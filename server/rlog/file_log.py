# -*- coding: utf-8 -*-
import os

class FileLog():
    _log_path = ''
    _handle = None

    def __init__(self, log_path):
        self._log_path = log_path
        log_folder = os.path.split(log_path)[0]
        if not os.path.exists(log_folder):
            raise IOError('folder does not exist!')
        if not os.path.exists(log_path):
            os.mknod(log_path) 

    def write(self, content):
        self._handle = open(self._log_path, 'a')
        self._handle.write(content)
        self._handle.close()
