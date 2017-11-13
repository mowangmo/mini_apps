import socketserver
import struct
import json
import os
from db import account_db
import configparser

class FtpServer(socketserver.BaseRequestHandler):   # 必须继承BaseRequestHandler
    coding='utf-8'
    server_dir='put_file'
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

    def useradd(self,args):
        print(args)
        name = args['name']
        size = args['size']
        password_uuid = args['password_uuid']

        home_path = os.path.normpath(os.path.join(
            os.path.dirname(self.BASE_DIR),'db','put_file',name
        ) )
        print(home_path)    #F:\code\python19\mini_apps\FTP\server\db\put_file

        if not os.path.exists(home_path):   #为用户创建家目录
            os.mkdir(home_path)
            print(home_path,'创建成功')

        conf_path = os.path.normpath(os.path.join(      #配置文件路径
            os.path.dirname(self.BASE_DIR),'conf','settings.ini'
        ))
        print(conf_path)    #D:\工作目录\code\mini_apps\FTP\server\conf\settings.ini
        config = configparser.ConfigParser()    #为用户生成配置文件
        config.read(conf_path)   #读取配置文件
        sections = config.sections()
        print(sections)

        if name not in sections:   #如果没有该用户则生成配置文件
            config.add_section(name)    #添加标题
            config[name] = {'size': size, 'home_path': home_path}   #添加内容
            with open(conf_path , 'a') as configfile:
                config.write(configfile)    #写入配置文件
                print('用户', name ,'已生成配置文件')

        if name not in account_db.all_account:      #在数据库中添加一个用户
            account_db.all_account[name] = password_uuid
            print(account_db.all_account)

    def put(self,args):
        filesize = args['filesize']
        name = args['name']
        file_path = os.path.normpath(os.path.join(
            self.BASE_DIR,
            'db',self.server_dir,name,
            args['filename']    #提取字典的文件名,
        ))

        recv_size = 0
        print('----->', file_path)
        with open(file_path, 'wb') as f:
            while recv_size < filesize:
                recv_data = self.request.recv(self.max_packet_size)
                f.write(recv_data)
                recv_size += len(recv_data)
                print('recvsize:%s filesize:%s' % (recv_size, filesize))



