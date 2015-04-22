# -*- coding: utf-8 -*-
import json

ERROR_PARAM = 1
ERROR_NOT_FOUND = 2
#progress actions
ACTIONS = ['status', 'register', 'start', 'stop']

def error(error_type, error_msg):
    info = dict()
    info['result'] = False
    info['type'] = error_type
    info['msg'] = error_msg
    return json.dumps(info)

def status():
    #todo
    pass

def register():
    pass

def socket_deal(data):
    info = '{"action":"status"}'
    try:
        info = json.loads(data)
    except Exception, e:
        return error(ERROR_PARAM, 'data is not json')
    print info
    if not isinstance(info, dict) or info.get('action', '') not in ACTIONS:
        return error(ERROR_PARAM, 'param action error')
    action = info['action']
    if action == 'status':
        return status()
    if action == 'register':
        return register()