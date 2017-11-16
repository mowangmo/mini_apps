import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from lib import my_optparse
from src import batch


if __name__ == '__main__':
    options = my_optparse.my_opt()  #对用户输入参数进行解析
    print(options)  #{'cmd': 'df -TH', 'host': 'b', 'group': 'a'}输入参数返回字典
    a = batch.Batch(options)  #调用主函数，进行批量操作
    print(a.parse_ini())








