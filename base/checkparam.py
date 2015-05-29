# -*- coding: utf-8 -*-
from optparse import OptionParser
import config
import re

class Param():
    __parser = ''
    
    def __init__(self):
        self.__parser = OptionParser()
        self.__parser.add_option('-t', '--task', dest='task', default='all', metavar='NAME', help='the task name, default value is "all" that means all task')
        self.__parser.add_option('-n', '--node', dest='node', default='root', metavar='NAME', help='the node name: user, root[default]')
        self.__parser.add_option('-s', '--server', dest='server', default='master', metavar='NAME', help='the server name: master[default], or slave')
        self.__parser.add_option('-f', '--flag', dest='flag', default='0', metavar='NAME', help='the task flag: 1, 2, 3...')
        self.__parser.add_option('--status', action='store_const', dest='option', const='status', default='status', help='show the progress status')
        self.__parser.add_option('--start', action='store_const', dest='option', const='start', help='start the progress')
        self.__parser.add_option('--stop', action='store_const', dest='option', const='stop', help='stop the progress')
        self.__parser.add_option('--restart', action='store_const', dest='option', const='restart', help='restart the progress')
    
    def check(self):
        options = self.__parser.parse_args()[0]
        #check node
        nodes = ['user', 'root']
        if not options.node in nodes:
            self.__parser.error('-n --node value %s should be user, root' % (options.node))
        #check server
        servers = ['master', 'slave']
        if not options.server in servers:
            self.__parser.error('-s --server value %s should be master or slave' % (options.server))
        #check task
        if options.task != 'all' and not config.task(options.task):
            self.__parser.error('-t --task value %s is not a task name' % (options.task))
        #check flag
        if not re.match(r'^\d*$', options.flag):
            self.__parser.error('-f --flag value %s shoul be a number' % (options.flag))
        options.flag = int(options.flag)
        #both root and task don't eixist
        if options.node == 'root' and options.task != 'all':
            self.__parser.error('when node is root, but  value %s shoul be a number' % (options.flag))
        return options