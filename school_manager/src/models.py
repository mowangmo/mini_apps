class Person:
    def __init__(self,name,sex,tel):
        self.name = name
        self.sex = sex
        self.tel = tel

class Student(Person):
    def __init__(self,name,sex,tel,salary):
        super().__init__(name,sex,tel,salary)
        self.salary = salary

class Teacher:
    def __init__(self,name,sex,tel):


class School:
    def __init__(self,name,place):
        self.name = name
        self.place = place



class Couse:
    def __init__(self,name,price,cycle):
        self.name = name
        self.price = price
        self.cycle = cycle



