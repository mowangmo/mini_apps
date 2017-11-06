import socketserver
import struct
import json
import os

class FtpServer(socketserver.BaseRequestHandler):   # 必须继承BaseRequestHandler
    coding='utf-8'
    server_dir='file_upload'
    max_packet_size=1024
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
    def handle(self):   # 必须有handle方法
        print(self.request)
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


ftpserver=socketserver.ThreadingTCPServer(('127.0.0.1',8082),FtpServer)
ftpserver.serve_forever()

