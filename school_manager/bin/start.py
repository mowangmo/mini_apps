#_*_coding:utf-8_*_

import os
import sys
from src.services import admin_service
from src.services import register_service
from src.services import student_service
from src.services import teacher_service

BASE_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

def menu():
    menu_info = '''
    0.用户注册
    1.管理员登录
    2.教师登录
    3.学生登录
    '''
    print(menu_info)

if __name__ == '__main__':
    menu_dic = {
        '0':register_service.main,
        '1':admin_service.login,
        '2':teacher_service.login,
        '3':student_service.login,
    }

    while True:
        menu()
        inp = input("-----欢迎登入校园管理系统----->>:").strip()
        if inp not in menu_dic : continue
        menu_dic[inp]()

