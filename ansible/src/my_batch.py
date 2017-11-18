import configparser
from conf import settings
from lib import my_ssh
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor,Executor

class Batch:
    def __init__(self,options):
        self.host = options.host
        self.group = options.group
        self.cmd = options.cmd

    def __str__(self):
        return self.host,self.group,self.cmd

    def parse_ini(self):
        if self.host:  #host有值并有多个是以逗号分隔
            h_list = self.host.split(',')   #提取出进来的主机
            # print('--host' ,h_list)
        if self.group:  #同上
            g_list = self.group.split(',')
            # print(g_list)
        if self.cmd:    #提取命令
            cmd = self.cmd
            # print(cmd)
        else:
            print('请输入命令!')

        config = configparser.ConfigParser()
        config.read(settings.server_ini)

        g_h_list = []

        for g in g_list:
            g_h_l = config.options(g)     #提取某个组下的所有主机
            # print('group host',g_h)   #['h1', 'h2']
            for h in g_h_l:
                g_h_list.append(h)    #将组下的主机加入列表

        # print('group host', g_h_list)

        group_host_list = h_list + g_h_list
        # print(group_host_list)  #['h1', 'h3', 'h1', 'h2'] 将host的主机和group的主机列表加起来

        finally_host_list = []      #进行去重
        for h in group_host_list:
            if h not in finally_host_list:
                finally_host_list.append(h)

        print('去重后的主机：',finally_host_list)

        return finally_host_list,cmd


