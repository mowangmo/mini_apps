#_*_coding:utf-8_*_

import time
import pickle
import os
from conf import settings
from src import unique_id

class Base_Model:   #父类
    def dump(self):     #将对象dump到文件
        file_path = os.path.join(self.db_path,str(self.uuid))     #设置dump的路径，id为文件名
        pickle.dump(self,open(file_path,'wb'))  #wb 以二进制写模式打开

    @classmethod    #类方法,无需对象，可通过类直接调用
    def all_obj_list(cls):
        all_obj_l = []
        for file_name in os.listdir(cls.db_path):   #将对象都加入到列表
            file_path = os.path.join(cls.db_path,file_name)
            all_obj_l.append(pickle.load(open(file_path,'rb')))     #rb  以二进制读模式打开
        return all_obj_l

