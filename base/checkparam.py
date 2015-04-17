# -*- coding: utf-8 -*-
from optparse import OptionParser

class Param():
    __options = ''
    __args = ''
    
    def __init__(self):
        parser = OptionParser()
        parser.add_option("--file", dest="filename", help="write report to FILE", metavar="FILE")  
        parser.add_option("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")  
        options, args = parser.parse_args()
        print options, args
    
    def check(self):
        pass