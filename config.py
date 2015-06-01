# -*- coding: utf-8 -*-
import time
import json
from base.checkconfig import Conf
from lib.rthread import Rthread

config_file = 'config/ran.config'
task_file = 'config/task.config'
local_file = 'config/local.config'
error_file = 'config/error.config'
settings = dict()
task_settings = dict()
local_settings = dict()
error_settings = dict()


def config(key):
    return settings.get(key, '')

def task(key):
    return task_settings.get(key, '')

def local(key):
    return local_settings.get(key, '')

def error(key, msg = ''):
    error_info = error_settings.get(key, {'num' : '1000', 'msg' : 'nothing'})
    if msg:
        error_info['msg'] = error_info['msg'] + ' --- ' + msg
    error_info['result'] = False
    return json.dumps(error_info)

def success(data = ''):
    info = dict()
    info['result'] = True
    info['msg'] = data
    info['num'] = '0'
    return json.dumps(info)

def _thread(self):
    conf = Conf()
    while True:
        #task config
        with open(task_file) as fp:
            task_config = fp.readlines()
        settings = conf.check_task(task_config)
        if not settings:
            print conf.get_error()
        else:
            self.task_settings = settings
        #local config
        with open(local_file) as fp:
            local_config = fp.readlines()
        settings = conf.check_local(local_config)
        if not settings:
            print conf.get_error()
        else:
            self.local_settings = settings
        time.sleep(self.settings.get('config_refresh_time'))

def init(self):
    conf = Conf()
    #init ran config
    with open(config_file) as fp:
        ran_config = fp.readlines()
    self.settings = conf.check_ran(ran_config)
    if not self.settings:
        print conf.get_error()
        exit(0)
    #init task config
    with open(task_file) as fp:
        task_config = fp.readlines()
    self.task_settings = conf.check_task(task_config)
    if not self.task_settings:
        print conf.get_error()
        exit(0)
    #init local config
    with open(local_file) as fp:
        local_config = fp.readlines()
    self.local_settings = conf.check_local(local_config)
    if not self.local_settings:
        print conf.get_error()
        exit(0)
    #init error config
    with open(error_file) as fp:
        error_config = fp.readlines()
    self.error_settings = conf.check_error(error_config)
    if not self.error_settings:
        print conf.get_error()
        exit(0)
    #init thread check task config
    if self.settings.get('config_refresh'):
        config_thread = Rthread(_thread, 'config_refresh', self)
        config_thread.start()

#super param
running = True