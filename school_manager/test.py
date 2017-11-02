# IND = 'ON'
# def checkind():
#     return (IND == 'ON')
# class Kls(object):
#      def __init__(self,data):
#         self.data = data
# def do_reset(self):
#     if checkind():
#         print('Reset done for:', self.data)
# def set_db(self):
#     if checkind():
#         self.db = 'new db connection'
#         print('DB connection made for:',self.data)
# ik1 = Kls(12)
# do_reset(ik1)
# set_db(ik1)


# IND = 'no'
# class Kls(object):
#     def __init__(self, data):
#         self.data = data
#     @staticmethod
#     def checkind():
#         return (IND == 'ON')
#     def do_reset(self):
#         if self.checkind():
#             print('Reset done for:', self.data)
#     def set_db(self):
#         if self.checkind():
#             self.db = 'New db connection'
#         print('DB connection made for: ', self.data)
# ik1 = Kls(12)
# ik1.do_reset()
# ik1.set_db()

class Kls(object):
    def __init__(self, data):
        self.data = data
    def printd(self):
        print(self.data)
    @staticmethod
    def smethod(*arg):
        print('Static:', arg)
    @classmethod
    def cmethod(*arg):
        print('Class:', arg)

ik = Kls(23)
ik.printd()
ik.smethod()
ik.cmethod()
Kls.smethod()
Kls.cmethod()