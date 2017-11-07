import socket
import struct
import json
import os
import uuid

class MYTCPClient:
    address_family = socket.AF_INET     #互联网模式
    socket_type = socket.SOCK_STREAM    #tcp
    allow_reuse_address = False
    max_packet_size = 8192
    coding='utf-8'
    request_queue_size = 5      #最多挂起5个

    def __init__(self, server_address, connect=True):
        self.server_address=server_address
        self.socket = socket.socket(self.address_family,
                                    self.socket_type)
        if connect:
            try:
                self.client_connect()
            except:
                self.client_close()
                raise   #报一个异常

    def client_connect(self):       #建立连接
        self.socket.connect(self.server_address)

    def client_close(self):         #关闭连接
        self.socket.close()

    def register(self):     #验证登录
        while True:
            name = input("请输入用户名>>: ").strip()
            passwd = input("请输入密码>>: ").strip()
            # name_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, name))   #通过uuid加密发送过去
            passwd_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, passwd))
            account_dict = {'name':name,'passwd':passwd_uuid}
            # print(account_dict)   #{'name': 'wangmo', 'passwd': '79320ea6-f27c-3294-a486-aaa1cbda61cc'}
            account_json = json.dumps(account_dict)     #序列化
            account_json_bytes = bytes(account_json,encoding=self.coding)   #转换为utf8的bytes才可以发送
            self.socket.send(account_json_bytes)    #将用户名和密码发送过去

            res = self.socket.recv(1024)    #接收服务端返回的结果
            res_json = res.decode(self.coding)
            res_dict = json.loads(res_json)
            print(res_dict)
            if res_dict['status'] == '0':
                print(res_dict['message'])
                break
            elif res_dict['status'] == '1':
                print(res_dict['message'])
                continue

    def run(self):
        while True:
            inp=input(">>: ").strip()   #put file1
            if not inp:continue
            l=inp.split()
            cmd=l[0]
            if hasattr(self,cmd):
                func=getattr(self,cmd)
                func(l)

    def put(self,args):     ##put file1
        cmd=args[0]
        filename=args[1]
        if not os.path.isfile(filename):
            print('file:%s is not exists' %filename)
            return
        else:
            filesize=os.path.getsize(filename)

        head_dic={'cmd':cmd,'filename':os.path.basename(filename),'filesize':filesize}
        print(head_dic)
        head_json=json.dumps(head_dic)
        head_json_bytes=bytes(head_json,encoding=self.coding)

        head_struct=struct.pack('i',len(head_json_bytes))
        self.socket.send(head_struct)
        self.socket.send(head_json_bytes)
        send_size=0
        with open(filename,'rb') as f:
            for line in f:
                self.socket.send(line)
                send_size+=len(line)
                print(send_size)
            else:
                print('upload successful')

if __name__ == '__main__':
    client=MYTCPClient(('127.0.0.1',8083))      #生成一个client对象，并建立socket连接
    client.register()
    client.run()        #client对象通过反射调用类中的方法