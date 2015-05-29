#-*- coding:utf-8 -*-
'''
normal function for ran connect
server connect by tcp socket
node connect by file socket
'''
import json

def node_transfer_data(option, server = '', node = '', task = ''):
    param = dict()
    param['option'] = option
    param['server'] = server
    param['node'] = node
    param['task'] = task
    return json.dumps(param)

def node_transfer_parser(data):
    try:
        param = json.loads(data)
    except Exception, e:
        return False
    if not param.get('option'):
        return False
    return param

def node_transfer_error(num, msg):
    info = dict()
    info['result'] = False
    info['num'] = num
    info['msg'] = msg
    return json.dumps(info)