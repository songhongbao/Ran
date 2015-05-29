#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import config
import ran

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    config.init(config)
    ran.main()