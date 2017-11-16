import configparser
from conf import settings

class Batch:
    def __init__(self,options):
        self.host = options.host
        self.group = options.group
        self.cmd = options.cmd

    def __str__(self):
        return self.host,self.group,self.cmd

    def parse_ini(self):
        if self.host:  #host有值并有多个是以逗号分隔
            h_list = self.host.split(',')
            # print(h_list)
        if self.group:  #同上
            g_list = self.group.split(',')

        config = configparser.ConfigParser()
        config.read(settings.server_ini)
        

