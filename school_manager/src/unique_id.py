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

        def 

