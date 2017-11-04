#_*_coding:utf-8_*_

import time
import pickle
import os
from conf import settings
from src import unique_id

class Base_Model:   #此模块主要为建立，保存，查看各种角色
    def dump(self):     #将对象dump到文件
        file_path = os.path.join(self.db_path,str(self.uuid))     #设置dump的路径，id为文件名
        pickle.dump(self,open(file_path,'wb'))  #wb 以二进制写模式打开

    @classmethod    #类方法,无需对象，可通过类直接调用
    def all_obj_list(cls):  #获取这个类的所有对象，通过类方法可以取到类变量
        all_obj_l = []
        for file_name in os.listdir(cls.db_path):   #将对象都加入到列表。通过cls来获取这个静态字段
            file_path = os.path.join(cls.db_path,file_name)
            all_obj_l.append(pickle.load(open(file_path,'rb')))     #rb  以二进制读模式打开
        return all_obj_l    #通过Admin.all_obj_list()调用获取

class Admin(Base_Model):    #管理员类，新增课程，新增老师等操作
    db_path = settings.ADMIN_DB_DIR     #将路径写到配置文件中，不要写死
    def __init__(self,username,passwd):
        self.username = username
        self.passwd = passwd
        self.set_up_time = time.strftime('%Y-%m-%d')    #2017-11-02
        self.id = unique_id.Admin_id(self.db_path) #此id为dump文件的用户名-----------------------这个id就是uuid为文件名的路径

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
        self.__income = 0 #学校的收入不可见，私有属性

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

class Course_to_teacher(Base_Model):    #课程跟老师的关系，因为一个老师可以教多个课程，如果要写到Teacher类下面，那么老师就只能教一个课程了
    db_path = settings.COURSE_TO_TEACHER_DB_DIR
    def __init__(self,course_id,school_id,teacher_id):
        self.id = unique_id.Course_to_teacher_id(self.db_path)
        self.course_id = course_id
        self.school_id = school_id
        self.teacher_id = teacher_id

    def course_to_teacher_list(self):   #课程和老师对应关系
        course_to_teacher_l = self.all_obj_list()
        if course_to_teacher_l:
            return [
                        course_to_teacher_l.course_id.find_uuid_obj(),  #返回这个老师所教的课程和班级
                        course_to_teacher_l.classes_id.find_uuid_obj()
                    ]
        return [None,None]

class Classes(Base_Model): #
    db_path = settings.CLASSES_DB_DIR
    def __init__(self,name,fee,school_id,course_to_teacher_list):
        self.id = unique_id.Classes_id(self.db_path)
        self.name = name
        self.fee = fee
        self.school_id = school_id
        self.course_to_teacher_list = course_to_teacher_list

class Sorce(Base_Model):    #分数类
    def __init__(self,id):
        self.id = id
        self.score_dict = {} #记录各个学科的分数

    def entering(self,course_to_teacher_id,number):     #录入分数
        self.score_dict[course_to_teacher_id] = number  #记录某科分数

    def get(self,course_to_teacher_id):     #获取分数
        return self.score_dict.get(course_to_teacher_id)    #字典的get方法

class Student(Base_Model):
    db_path = settings.SCHOOL_DB_DIR
    def __init__(self,name,age,qq,classes_id):
        self.id = unique_id.Student_id(self.db_path)
        self.name = name
        self.age = age
        self.qq = qq
        self.classes_id = classes_id
        self.score = Sorce(self.id)








