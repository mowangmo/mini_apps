#_*_coding:utf-8_*_



import os
import sys

BASE_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from src import login_fun




if __name__ == '__main__':
    print("----------欢迎使用ftp----------""\n")
    name = input('name >>:')
    passwd = input('pass >>:')
    login_fun.login(name,passwd)

