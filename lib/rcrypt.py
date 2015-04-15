#-*- coding:utf-8 -*-
#!/usr/bin/python
from Crypto.Cipher import AES
import hashlib
import random

AES_MODE_ECB = 1
AES_MODE_CBC = 2
AES_MODE_CFB = 3
AES_MODE_PGP = 4
AES_MODE_OFB = 5
AES_MODE_CTR = 6
AES_MODE_OPENPGP = 7
AES_KEY = 'RanShy is lucky!'
AES_DISTURB = '\0'
HASH_MODE_MD5 = 1
HASH_MODE_SHA1 = 2
HASH_KEY = 'RanShy is lucky!'
RAN_MODE_32 = 1
RAN_MODE_64 = 2
RAN_CODE = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@$_()[]{}/'
RAN_DISTURB = '*'
RAN_CHANNEL_TOKEN = 'TOKEN'
RAN_CHANNEL_SESSION = 'SESSION'
RAN_CHANNEL_INFO = 'INFO'
RAN_CHANNEL_COUNT = 'COUNT'

class Rcrypt():
    def __init__(self):
        #aes setting
        #aes key length must be 16(AES-128), 24(AES-192), 32(AES-256)
        self.aes_key = AES_KEY
        self.aes_mode = AES_MODE_CBC
        self.aes_disturb = AES_DISTURB
        #hash setting
        #hash key is salt
        self.hash_key = HASH_KEY
        self.hash_mode = HASH_MODE_MD5
        #ran setting
        #ran key is char list
        self.ran_code = RAN_CODE
        self.ran_mode = RAN_MODE_32
        self.ran_channel = RAN_CHANNEL_TOKEN[0 : 2]
        self.ran_disturb = RAN_DISTURB

    def aes_encrypt(self, value):
        #the value must be a multiple of 16 in length
        add = 16 - len(value) % 16
        value += (self.aes_disturb * add)
        ran_aes = AES.new(self.aes_key, self.aes_mode, IV='q'*16)
        return ran_aes.encrypt(value)

    def aes_decrypt(self, value):
        ran_aes = AES.new(self.aes_key, self.aes_mode, IV='q'*16)
        return ran_aes.decrypt(value).rstrip(AES_DISTURB)
    
    def hash(self, value):
        if self.hash_mode == HASH_MODE_MD5:
            ran_hash = hashlib.md5()
        else:
            ran_hash = hashlib.sha1()
        ran_hash.update(str(value))
        return ran_hash.hexdigest()
    
    def hash_key(self, value):
        if self.hash_mode == HASH_MODE_MD5:
            ran_hash = hashlib.md5()
        else:
            ran_hash = hashlib.sha1()
        value = str(value) + str(self.hash_key)
        ran_hash.update(value)
        return ran_hash.hexdigest()
    
    def hash_salt(self, value, salt):
        if self.hash_mode == HASH_MODE_MD5:
            ran_hash = hashlib.md5()
        else:
            ran_hash = hashlib.sha1()
        value = str(value) + str(self.hash_key)
        ran_hash.update(value)
        value = ran_hash.hexdigest()
        value = str(value) + str(salt)
        if self.hash_mode == HASH_MODE_MD5:
            ran_hash = hashlib.md5()
        else:
            ran_hash = hashlib.sha1()
        ran_hash.update(value)
        return ran_hash.hexdigest()
    
    def ran_encrypt(self, flag):
        if len(flag) >= 10:
            flag = str(flag)[0 : 10]
        else:
            flag = str(flag) + (10 - len(flag)) * self.ran_disturb
        #get the secret_token
        secret_token = ''
        if self.ran_mode == RAN_MODE_32:
            num = 32 - 10 - 2
        else:
            num = 64 - 10 - 2
        while num:
            secret_token += self.ran_code[random.randint(0, len(self.ran_code) - 1)]
            num -= 1
        #get the channel_token
        pre_code = self.hash(secret_token[0 : 10])[0 : 5]
        suf_code = self.hash(secret_token[10 : ])[0 : 5]
        channel_token = self.hash(self.ran_channel + pre_code + suf_code)[0 : 2]
        #get the key_token
        key_token = ''
        code = self.ran_disturb + self.ran_code
        secret = pre_code + suf_code
        for i in range(10):
            pos = code.find(flag[i : i + 1]) + int(secret[i : i + 1], 16) * 2
            key_token += code[pos : pos + 1]
        result = dict()
        result['key'] = self.ran_channel + flag + secret_token
        result['value'] = channel_token + key_token + secret_token
        return result
    
    def ran_decrypt(self, flag, value):
        if len(flag) >= 10:
            flag = str(flag)[0 : 10]
        else:
            flag = str(flag) + (10 - len(flag)) * self.ran_disturb
        #init the value
        channel_token = value[0 : 2]
        key_token = value[2 : 12]
        secret_token = value[12 : ]
        pre_code = self.hash(secret_token[0 : 10])[0 : 5]
        suf_code = self.hash(secret_token[10 : ])[0 : 5]
        secret = pre_code + suf_code
        code = self.ran_disturb + self.ran_code
        #get the flag
        c_flag = ''
        for i in range(10):
            pos = code.find(key_token[i : i + 1]) - int(secret[i : i + 1], 16) * 2
            c_flag += code[pos : pos + 1]
        #get the channel
        c_channel_token = self.hash(self.ran_channel + pre_code + suf_code)[0 : 2]
        if c_flag != flag or c_channel_token != channel_token:
            return False
        key = self.ran_channel + flag + secret_token
        return key


    
if __name__ == '__main__':
    ran_crypt = Rcrypt()  # 初始化密钥
#     e = ran_crypt.aes_encrypt('dsads4')
#    d = ran_crypt.aes_decrypt(e)
#    print "加密:",e
#    print "解密:",d
#    print ran_crypt.hash(0)
    a= ran_crypt.ran_encrypt('1234123')
    b= ran_crypt.ran_decrypt('1234123', a['value'])
    print a
    print b
    