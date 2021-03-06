# -*- coding: utf-8 -*-
import re
import os
import sys

class Conf():
    _config = dict()
    _error_msg = ''
    _task_propertys = ['progress', 'thread']
    _task_list = []
    
    #deal ran config
    #ran config only support strict pattern: key=value
    def _deal(self, line, num):
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            return True
        if len(line.split('=')) != 2:
            return False
        key, value = line.split('=')
        key = key.strip()
        value = value.strip()
        self._config[key] = (value, num)
        return True
    
    #deal task config
    #task config only support strict pattern: taskname.property=numbers
    def _task_deal(self, config, key, value):
        if len(key.split('.')) != 2:
            return False
        task_name, task_property = key.split('.')
        #property need be in _task_propertys
        if not task_property in self._task_propertys:
            return False
        #property need be numbers
        if not re.match(r'^[1-9]\d*$', value):
            return False
        value = int(value)
        #task need be in task folder
        if not task_name in self._task_list:
            return False
        #all is ok, register to the config
        if not config.get(task_name):
            config[task_name] = dict()
            config[task_name]['progress'] = 1
            config[task_name]['thread'] = 1
        config[task_name][task_property] = value
        return config
    
    #deal local config
    #local config can support normal pattern: key1.key2.key3...keyn=valuel
    def _local_deal(self, config, key, value):
        if len(key) == 1:
            config[key[0]] = value
        else:
            if not config.get(key[0]) or not isinstance(config[key[0]], dict):
                config[key[0]] = dict()
            config[key[0]] = self._local_deal(config[key[0]], key[1:], value)
        return config
    
    #deal error config
    #error config value include error const, and error info
    def _error_deal(self, config, key, value):
        if len(value.split(':')) != 2:
            return False
        error_key, error_value = value.split(':')
        error_key = error_key.strip()
        error_value = error_value.strip()
        config[error_key] = dict()
        config[error_key]['num'] = key
        config[error_key]['msg'] = error_value
        return config
    
    #init the task file name list
    def _init_task_folder(self):
        self._task_list = []
        for task_name in os.listdir('task'):
            if task_name[-3 : ] == '.py':
                self._task_list.append(task_name[0 : -3])
    
    #config check false, set the errors
    def _set_error(self, value, line=0, name='ran'):
        if line:
            self._error_msg = name + '.config line ' + str(line) + ' error: ' + str(value)
        else:
            self._error_msg = 'check ' + name + '.config error:\n' + str(value)
    
    #if config check false, you can get errors by the function
    #the error info can be write in the ran log
    def get_error(self):
        return self._error_msg

    #ran config check is complex
    def check_ran(self, lines):
        self._config = dict()
        num = 1
        for line in lines:
            if not self._deal(line, num):
                self._set_error(line, num)
                return False
            num += 1
        config = dict()
        #set progress dir
        config['dir'] = sys.path[0]
        #task refresh
        value, num = self._config.get('config_refresh', ('no', 0))
        if value != 'yes' and value != 'no':
            self._set_error(value, num)
            return False
        config['config_refresh'] = False if value == 'no' else True
        #task refresh time
        value, num = self._config.get('config_refresh_time', ('60', 0))
        if not re.match(r'^[1-9]\d*$', value):
            self._set_error(value, num)
            return False
        config['config_refresh_time'] = int(value)
        #socket_folder
        value, num = self._config.get('socket_folder', ('tmp', 0))
        if value.find('/') == 0:
            config['socket_folder'] = value
        else:
            config['socket_folder'] = config['dir'] + '/' + value
        if not os.path.exists(config['socket_folder']):
            self._set_error(value + ' folder not exist', num)
            return False
        #socket_port
        value, num = self._config.get('socket_port', ('7664', 0))
        if not re.match(r'^[1-9]\d*$', value):
            self._set_error(value, num)
            return False
        config['socket_port'] = int(value)
        #log_file_folder
        value, num = self._config.get('log_file_folder', ('log', 0))
        #if not os.path.exists(file_folder):
        config['log_file_folder'] = value
        #log_udp_host
        value, num = self._config.get('log_udp_host', ('127.0.0.1', 0))
        config['log_udp_host'] = value
        #log udp port
        value, num = self._config.get('log_udp_port', ('5202', 0))
        if not re.match(r'^[1-9]\d*$', value):
            self._set_error(value, num)
            return False
        config['log_udp_port'] = int(value)
        return config
    
    def check_task(self, lines):
        self._config = dict()
        num = 1
        for line in lines:
            if not self._deal(line, num):
                self._set_error(line, num, 'task')
                return False
            num += 1
        self._init_task_folder()
        config = dict()
        for key, value in self._config.iteritems():
            if not self._task_deal(config, key, value[0]):
                self._set_error(key + '=' + value[0], value[1], 'task')
                return False
        return config

    def check_local(self, lines):
        self._config = dict()
        num = 1
        for line in lines:
            if not self._deal(line, num):
                self._set_error(line, num, 'local')
                return False
            num += 1
        config = dict()
        for key, value in self._config.iteritems():
            self._local_deal(config, key.split('.'), value[0])
        return config
    
    def check_error(self, lines):
        self._config = dict()
        num = 1
        for line in lines:
            if not self._deal(line, num):
                self._set_error(line, num, 'local')
                return False
            num += 1
        config = dict()
        for key, value in self._config.iteritems():
            self._error_deal(config, key, value[0])
        return config