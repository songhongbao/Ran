# -*- coding: utf-8 -*-
import time
import file_log
import udp_log

LOG_OK = 1
LOG_NORMAL = 2
LOG_WARN = 3
LOG_ERROR = 4
#use file log, or use udp log
LOG_FILE = 'file'
LOG_UDP = 'udp'
LOG_DEFAULT = 'udp'
LOG_FILE_SETTING = '/tmp/ran.log'
LOG_UDP_SETTING = ('121.42.153.188', 5202)
#LOG TYPE, you can add what you want
LOG_TYPE_PROGRESS = 'progress'
LOG_TYPE_API = 'api'
LOG_TYPE_MEMCACHE = 'memcache'
LOG_TYPE_MYSQL = 'mysql'
LOG_TYPE_REDIS = 'redis'
LOG_TYPE_RABBITMQ = 'rabbitmq'
LOG_TYPE_FSOCKET = 'filesocket'


def color(msg, msg_type):
    color_list = {LOG_OK : '32', LOG_NORMAL : '36', LOG_WARN : '33', LOG_ERROR : '31'}
    color = color_list[msg_type]
    return '%s[%s;2m%s%s[0m' % (chr(27), color, str(msg), chr(27))

def gen_msg(destination, log_type, spend, operate, data_detail, msg_success, suffix = ''):
    current_time = time.strftime('%X', time.localtime(time.time()+time.timezone+28800))
    msg = str(current_time) + ' [rpc]>' + destination + ' [' + log_type + '] '
    if spend < 0.1:
        msg += color('<%.4f>' % spend, LOG_OK)
    elif 0.1 <= spend < 1.0:
        msg += color('<%.4f>' % spend, LOG_NORMAL)
    elif 1.0 <= spend < 2.0:
        msg += color('<%.4f>' % spend, LOG_WARN)
    else:
        msg += color('<%.4f>' % spend, LOG_ERROR)
    msg += ' ' + operate
    if msg_success:
        msg += color(' OK ', LOG_OK)
    else:
        msg += color(' ERROR ', LOG_ERROR)
    msg += '# ' + data_detail + ' '
    if suffix:
        msg += '(' + suffix + ')'
    return msg

if LOG_DEFAULT == LOG_FILE:
    ran_log = file_log.FileLog(LOG_FILE_SETTING)
else:
    ran_log = udp_log.UdpLog(LOG_UDP_SETTING)

def write(destination = '127.0.0.1', send_type = LOG_TYPE_PROGRESS, spend = 0.000, operate='', data_detail='', msg_success=True, suffix = ''):
    if len(data_detail) > 1000:
        data_detail = data_detail[0:1000]
    content = gen_msg(destination, send_type, spend, operate, data_detail, msg_success, suffix)
    if isinstance(content, unicode):
        content = content.encode('utf-8')
    content = content.replace('\r', '\\r').replace('\n', '\\n')
    content += '\n'
    ran_log.write(content)
