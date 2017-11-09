import socketserver
import struct
import json
import os
from db import account_db

class FtpServer(socketserver.BaseRequestHandler):   # 必须继承BaseRequestHandler
    coding='utf-8'
    server_dir='file_upload'
    max_packet_size=1024
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    def handle(self):   # 必须有handle方法
        print('与client建立连接。。。')
        print(self.request)
        self.register()     #调用登录方法

        while True:
            data=self.request.recv(4)   #接收报头
            data_len=struct.unpack('i',data)[0]     #获取报头大小
            head_json=self.request.recv(data_len).decode(self.coding)
            head_dic=json.loads(head_json)
            # print(head_dic)
            cmd=head_dic['cmd']     #输入的命令
            if hasattr(self,cmd):    #判断object中有没有一个cmd字符串对应的方法或属性
                func=getattr(self,cmd)
                func(head_dic)

    def register(self):     #验证登录
        while True:
            account = self.request.recv(1024)
            account_json = account.decode(self.coding)
            account_dict = json.loads(account_json)
            # print(account_dict,type(account_dict))     #取到用户名和密码
            #"{\"name\": \"wangmo\", \"passwd\": \"4dfc6b14-7213-3363-8009-b23c56e3a1b1\"}"
            name = account_dict['name']
            passwd = account_dict['passwd']

            if passwd == account_db.all_account.get(name):
                res = {'name':name,'status':'0','message':'用户验证成功!'}
                print(res['message'])
                res_json = json.dumps(res)  # 将验证结果发送给客户端
                res_json_bytes = bytes(res_json, encoding=self.coding)
                self.request.sendall(res_json_bytes)
                break   #验证过了则退出走下一步
            else:
                res = {'name':name,'status': '1', 'message': '用户名或密码输入有误!'}
                print(res['message'])
                res_json = json.dumps(res)      #将验证结果发送给客户端
                res_json_bytes = bytes(res_json, encoding=self.coding)
                self.request.sendall(res_json_bytes)
                continue    #验证没通过，继续进行验证

    def put(self,args):
        file_path = os.path.normpath(os.path.join(
            self.BASE_DIR,
            self.server_dir,
            args['filename']    #提取字典的文件名
        ))

        filesize = args['filesize']
        recv_size = 0
        print('----->', file_path)
        with open(file_path, 'wb') as f:
            while recv_size < filesize:
                recv_data = self.request.recv(self.max_packet_size)
                f.write(recv_data)
                recv_size += len(recv_data)
                print('recvsize:%s filesize:%s' % (recv_size, filesize))



