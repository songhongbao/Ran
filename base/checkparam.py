# -*- coding: utf-8 -*-
from optparse import OptionParser
import config

class Param():
    __parser = ''
    
    def __init__(self):
        self.__parser = OptionParser()
        self.__parser.add_option('-t', '--task', dest='task', default='all', metavar='NAME', help='the task name, default value is "all" that means all task')
        self.__parser.add_option('-n', '--node', dest='node', default='user', metavar='NAME', help='the node name: user[default], root, parent, or child')
        self.__parser.add_option('--status', action='store_const', dest='option', const='status', default='status', help='show the progress status')
        self.__parser.add_option('--start', action='store_const', dest='option', const='start', help='start the progress')
        self.__parser.add_option('--stop', action='store_const', dest='option', const='stop', help='stop the progress')
        self.__parser.add_option('--restart', action='store_const', dest='option', const='restart', help='restart the progress')
    
    def check(self):
        options = self.__parser.parse_args()[0]
        #check node
        nodes = ['user', 'root', 'parent', 'child']
        if not options.node in nodes:
            self.__parser.error('-n --node value %s should be user, root, parent, or child' % (options.node))
        #check task
        if options.task != 'all' and not config.task(options.task):
            self.__parser.error('-t --task value %s is not a task name' % (options.task))
        return options