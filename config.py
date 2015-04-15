# -*- coding: utf-8 -*-
import sys
import os
import time

cur_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(cur_path + '/server')
sys.path.append(cur_path + '/lib')

from rthread import Rthread

config_file = 'config/ran.config'
script_file = 'config/script.config'
settings = dict()
script_settings = dict()

def get(key):
    return settings.get(key, '')

def script(key):
    return script_settings.get(key, '')

def deal(line, script = False):
    line = line.strip()
    if len(line) == 0 or line[0] == '#':
        return True
    if len(line.split('=')) != 2:
        return False
    key, value = line.split('=')
    key = key.strip()
    value = value.strip()
    if script:
        script_settings[key] = value
    else:
        settings[key] = value
    return True

def main():
    with open(config_file) as fp:
        line_num = 1
        for line in fp:
            if not deal(line):
                raise ValueError('ran.config line ' + str(line_num) + ' error:\n' + line)
        line_num += 1
    init(False)
    config_thread = Rthread(init, 'config_refresh')
    config_thread.start()
    #time wait the thread first done
    time.sleep(0.2)

def init(is_thread = True):
    refresh = int(get('script_refresh'))
    refresh_time = int(get('script_refresh_time'))
    while True:
        with open(script_file) as fp:
            line_num = 1
            for line in fp:
                if not deal(line, True):
                    raise ValueError('ran.config line ' + str(line_num) + ' error:\n' + line)
                line_num += 1
            if refresh != 1 or is_thread == False:
                return
            time.sleep(refresh_time)


main()