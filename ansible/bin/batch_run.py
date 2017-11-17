#_*_coding:utf-8_*_
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from lib import my_optparse
from src import my_batch


if __name__ == '__main__':
    options = my_optparse.my_opt()  #对用户输入参数进行解析
    print('用户输入的参数：',options)  #{'cmd': 'df -TH', 'host': 'b', 'group': 'a'}输入参数返回字典
    batch_obj = my_batch.Batch(options)  #调用主函数，生成一个对象，进行批量操作
    parse_ini = batch_obj.parse_ini()   #调用解析配置文件方法








