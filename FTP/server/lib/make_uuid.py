import uuid

def set_uuid(passwd):
    return str(uuid.uuid3(uuid.NAMESPACE_DNS,passwd))   #基于字符串生成唯一标识

# a = set_uuid('123456')
# print(a)
#
# b = set_uuid('123456')
# print(b)

# 79320ea6-f27c-3294-a486-aaa1cbda61cc
# 79320ea6-f27c-3294-a486-aaa1cbda61cc