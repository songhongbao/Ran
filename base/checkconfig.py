# -*- coding: utf-8 -*-
import re

class Conf():
    __config = dict()
    __error_msg = ''
    
    def __deal(self, line, num):
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            return True
        if len(line.split('=')) != 2:
            return False
        key, value = line.split('=')
        key = key.strip()
        value = value.strip()
        self.__config[key] = (value, num)
        return True
    
    def __script_deal(self, config, key, value):
        if len(key) == 1:
            config[key[0]] = value
        else:
            if not config.get(key[0]) or not isinstance(config[key[0]], dict):
                config[key[0]] = dict()
            config[key[0]] = self.__script_deal(config[key[0]], key[1:], value)
        return config
    
    def __set_error(self, value, line = 0):
        if line:
            self.__error_msg = 'ran.config line ' + str(line) + ' error: ' + str(value)
        else:
            self.__error_msg = 'check config error:\n' + str(value)
    
    def get_error(self):
        return self.__error_msg

    def check_ran(self, lines):
        self.__config = dict()
        num = 1
        for line in lines:
            if not self.__deal(line, num):
                self.__set_error(line, num)
                return False
            num += 1
        config = dict()
        #script refresh
        value, num = self.__config.get('script_refresh', ('no', 0))
        if value != 'yes' and value != 'no':
            self.__set_error(value, num)
            return False
        config['script_refresh'] = False if value == 'no' else True
        #script refresh time
        value, num = self.__config.get('script_refresh_time', ('60', 0))
        if not re.match(r'^[1-9]\d*$', value):
            self.__set_error(value, num)
            return False
        config['script_refresh_time'] = int(value)
        #socket_folder
        value, num = self.__config.get('socket_folder', ('tmp', 0))
        config['socket_folder'] = value
        #socket_port
        value, num = self.__config.get('socket_port', ('7664', 0))
        if not re.match(r'^[1-9]\d*$', value):
            self.__set_error(value, num)
            return False
        config['socket_port'] = int(value)
        #log_file_folder
        value, num = self.__config.get('log_file_folder', ('log', 0))
        config['log_file_folder'] = value
        #log_udp_host
        value, num = self.__config.get('log_udp_host', ('127.0.0.1', 0))
        config['log_udp_host'] = value
        #log udp port
        value, num = self.__config.get('log_udp_port', ('5202', 0))
        if not re.match(r'^[1-9]\d*$', value):
            self.__set_error(value, num)
            return False
        config['log_udp_port'] = int(value)
        return config
    
    def check_script(self, lines):
        self.__config = dict()
        num = 1
        for line in lines:
            if not self.__deal(line, num):
                self.__set_error(line, num)
                return False
            num += 1
        config = dict()
        for key, value in self.__config.iteritems():
            self.__script_deal(config, key.split('.'), value[0])
        return config
