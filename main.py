#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import config
import ran
import time

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    config.init(config)
    ran.run()
    while True:
        print config.task_settings
        print config.local_settings
        print '\n'
        time.sleep(2)