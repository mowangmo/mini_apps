import paramiko


class Ssh_server:
    def __init__(self,hostname,username,password,port=22):
        self.hostname = hostname
        self.password = password
        self.port = port
        self.username = username
        self.ssh = paramiko.SSHClient() # 创建SSH对象
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
        self.ssh.connect(self.hostname,self.username,self.password,self.port)   # 连接服务器
        self.objsftp = self.ssh.open_sftp()     #

    def run_cmd(self):
        pass

