#encoding:utf8

import paramiko

class Ssh_server:
    def __init__(self,hostname,port,username,password):
        self.hostname = hostname
        self.password = password
        self.port = int(port)
        self.username = username
        self.ssh = paramiko.SSHClient() # 创建SSH对象
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
        self.ssh.connect(self.hostname,self.port,self.username,self.password)   # 连接服务器
        self.ssh_sftp=self.ssh.open_sftp()

    def run_cmd(self,cmd):  #cmd为传入的命令
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.read()

    def put(self,localpath,remotepath): #上传方法
        self.ssh_sftp.put(localpath,remotepath)

    def get(self,remotepath,localpath): #下载方法
        self.ssh_sftp.get(remotepath,localpath)

    def close(self):    #关闭连接
        self.ssh_sftp.close()
        self.ssh.close()

# if __name__ == '__main__':
#     ssh_obj = Ssh_server('172.16.160.99','22','root','!QAZ2wsx')
#     res = ssh_obj.run_cmd('df -h')
#     print(res.decode('utf-8'))
#     ssh_obj.close()