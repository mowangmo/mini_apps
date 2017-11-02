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

class Admin(Base_Model):
    db_path = settings.ADMIN_DB_DIR
    def __init__(self,username,passwd):
        self.username = username
        self.passwd = passwd
        self.set_up_time = time.strftime('%Y-%m-%d')    #2017-11-02
        self.id = unique_id.Admin_id(self.db_path) #此id为dump文件的用户名

    @staticmethod   #静态方法，跟类方法相似，不用传参数，用于校验较多
    def login():
        try:
            name = input('请输入用户名：').strip()
            passwd = input('请输入密码：').strip()

            for obj in Admin.all_obj_list():
                if obj.username == name and obj.passwd == passwd:   #校验密码是否正确
                    status = True
                    error = ''
                    data = '登录成功'
                    break
            else:
                raise Exception('用户名或密码错误')     #执行完所有for循环后执行else
        except Exception as e :
            status = False
            error = str(e)
            data = ''
        return {'status':status,'error':error,'data':data}      #相当于返回一个状态码

class School(Base_Model):
    db_path = settings.SCHOOL_DB_DIR
    def __init__(self,name,site):
        self.id = unique_id.School_id(self.db_path)
        self.name = name
        self.site = site
        self.set_time = time.strftime('%Y-%m-%d %X')

    def __str__(self):
        return self.name

class Teacher(Base_Model):
    db_path = settings.TEACHER_DB_DIR
    def __init__(self,name,level):
        self.id = unique_id.Teacher_id(self.db_path)
        self.name = name
        self.level = level
        self.set_time = time.strftime('%Y-%m-%d %X')

class Course(Base_Model):
    db_path = settings.CLASSES_DB_DIR
    def __init__(self,name,price,period,school_id):
        self.id = unique_id.Classes_id(self.db_path)
        self.name = name
        self.price = price
        self.period = period
        self.school_id = school_id

class Course_to_teacher(Base_Model):    #课程跟老师的关系
    db_path = settings.COURSE_TO_TEACHER_DB_DIR
    def __init__(self,course_id,school_id):
        self.id = unique_id.Course_to_teacher_id(self.db_path)
        self.course_id = course_id
        self.school_id = school_id

    def course_to_teacher_list(self):   #老师下面有哪些课和班级
        course_to_teacher_l = self.all_obj_list()
        if course_to_teacher_l:
            return [
                        course_to_teacher_l.course_id.find_uuid_obj(),
                        course_to_teacher_l.classes_nid.find_uuid_obj()
                    ]
        return [None,None]






