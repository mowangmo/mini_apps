#_*_coding:utf-8_*_
import os

#设置dump的路径，方便以后更改
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMIN_DB_DIR=os.path.join(BASE_DIR,'db','admin')
SCHOOL_DB_DIR=os.path.join(BASE_DIR,'db','school')
TEACHER_DB_DIR=os.path.join(BASE_DIR,'db','teacher')
COURSE_DB_DIR=os.path.join(BASE_DIR,'db','course')
COURSE_TO_TEACHER_DB_DIR=os.path.join(BASE_DIR,'db','course_to_teacher')
CLASSES_DB_DIR=os.path.join(BASE_DIR,'db','classes')
STUDENT_DB_DIR=os.path.join(BASE_DIR,'db','student')


# if __name__ == '__main__':
#     print(ADMIN_DB_DIR)