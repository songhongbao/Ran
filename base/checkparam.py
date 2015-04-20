# -*- coding: utf-8 -*-
from optparse import OptionParser

class Param():
    __parser = ''
    
    def __init__(self):
        self.__parser = OptionParser()
        self.__parser.add_option('-t', '--task', dest='task', default='all', metavar='NAME', help='the task name, default value is "all" that means all task')
        self.__parser.add_option('-n', '--node', dest='node', default='root', metavar='NAME', help='the node name: root[default], parent, or child')
        self.__parser.add_option('--status', action='store_const', dest='option', const='status', default='status', help='show the progress status')
        self.__parser.add_option('--start', action='store_const', dest='option', const='start', help='start the progress')
        self.__parser.add_option('--stop', action='store_const', dest='option', const='stop', help='stop the progress')
        self.__parser.add_option('--restart', action='store_const', dest='option', const='restart', help='restart the progress')
    
    def check(self):
        options = self.__parser.parse_args()[0]
        nodes = ['root', 'parent', 'child']
        if not options.node in nodes:
            self.__parser.error('-n --node value should be root, parent, or child')