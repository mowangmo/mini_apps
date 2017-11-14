from socket import *
#
# c = socket()
# c.connect(('127.0.0.1', 8080))
#
# while True:
#     msg=input('>>: ').strip()
#     if not msg:continue
#     c.send(msg.encode('utf-8'))
#     data=c.recv(1024)
#     print(data.decode('utf-8'))
#
# c.close()


c = socket()
c.connect(('127.0.0.1',8000))
while True:
    msg = input('>>:').strip()
    if not msg:continue
    c.send(msg.encode('utf-8'))
    data = c.recv(1024)
    print(data.decode('utf-8'))
c.close()