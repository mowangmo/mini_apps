class Classmethod_Demo():
    role = 'dog'

    @classmethod
    def func(cls):
        print(cls.role)

Classmethod_Demo.func()

class Staticmethod_Demo():
    role = 'dog'

    @staticmethod
    def func():
        print("当普通方法用")

Staticmethod_Demo.func()