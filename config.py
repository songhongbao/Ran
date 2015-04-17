# -*- coding: utf-8 -*-
import time
from base.checkconfig import Conf
from lib.rthread import Rthread

config_file = 'config/ran.config'
script_file = 'config/script.config'
settings = dict()
script_settings = dict()

def config(key):
    return settings.get(key, '')

def script(key):
    return script_settings.get(key, '')

def thread(self):
    conf = Conf()
    while True:
        with open(script_file) as fp:
            script_config = fp.readlines()
        settings = conf.check_script(script_config)
        if not settings:
            print conf.get_error()
        else:
            self.script_settings = settings
        time.sleep(self.settings.get('script_refresh_time'))

def init(self):
    conf = Conf()
    #init ran config
    with open(config_file) as fp:
        ran_config = fp.readlines()
    self.settings = conf.check_ran(ran_config)
    if not self.settings:
        print conf.get_error()
        exit(0)
    #init script config
    with open(script_file) as fp:
        script_config = fp.readlines()
    self.script_settings = conf.check_script(script_config)
    if not self.script_settings:
        print conf.get_error()
        exit(0)
    #init thread check script config
    if self.settings.get('script_refresh'):
        config_thread = Rthread(thread, 'config_refresh', self)
        config_thread.start()
