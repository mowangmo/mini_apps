#_*_coding:utf-8_*_

import uuid
import hashlib
import time

def set_uuid():
    return str(uuid.uuid1()) #基于时间戳生成随机数

def set_md5():
    random = hashlib.md5()
    random.update(bytes(str(time.time()),encoding='utf-8')) #也以时间戳的方式生成随机数
    return random.hexdigest()

if __name__ == '__main__':
    a = set_uuid()
    print(a)
    b = set_md5()
    print(b)