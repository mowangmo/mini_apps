from lib import commons
import os
import pickle

class Id:
    def __init__(self,obj,db_path):
        obj_list = [    #静态属性
            'admin', 'school', 'teacher', 'course', 'course_to_teacher', 'classes', 'student'
        ]
        if obj not in obj_list:      #如果创建的对象不再列表中则抛出异常
            raise Exception('对象输入有误！请选择：%s'  % ','  .join(obj_list))    #对象输入有误！请选择：admin,school,teacher,course,course_to_teacher,classes,student

        self.obj = obj
        self.uuid = commons.set_uuid()
        self.db_path = db_path

        def __str__(self):      #输出字符串而非内存地址
            return self.uuid

        def find_uuid_obj(self):    #通过uuid查找对应的对象
            for file_name in os.listdir(self.db_path): #相当于ls
                if file_name == self.uuid:
                    return pickle.load(open(os.path.join(self.db_path,file_name),'rb'))     #以二进制读模式打开
            return None

class Admin_id(Id):
    def __init__(self,db_path):
        super(Admin_id,self).__init__('admin',db_path)

class School_id(Id):
    def __init__(self,db_path):
        super(School_id,self).__init__('School',db_path)

class Teacher_id(Id):
    def __init__(self,db_path):
        super(Teacher_id,self).__init__('Teacher',db_path)

class Course_id(Id):
    def __init__(self,db_path):
        super(Course_id,self).__init__('Course',db_path)

class Course_to_teacher_id(Id):
    def __init__(self,db_path):
        super(Course_to_teacher_id,self).__init__('Course_to_teacher',db_path)

class Classes_id(Id):
    def __init__(self,db_path):
        super(Classes_id,self).__init__('Classes',db_path)

class Student_id(Id):
    def __init__(self,db_path):
        super(Student_id,self).__init__('Student',db_path)