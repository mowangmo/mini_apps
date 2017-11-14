from multiprocessing import Process
import time
import random
from socket import *

# def piao(name):
#     print('%s is piaoing' %name)
#     time.sleep(random.randint(1,3))
#     print('%s is over' %name)
#
# if __name__ == '__main__':
#     p = Process(target=piao,args=('alex',))
#     p.start()
#     print('zhu')

# class MyProcess(Process):
#     def __init__(self,name):
#         super(MyProcess,self).__init__()
#         self.name = name
#     def run(self):
#         print('%s is piaoing' % self.name)
#         time.sleep(random.randint(1, 3))
#         print('%s is over' % self.name)
#
# if __name__ == '__main__':
#     p = MyProcess('P1')
#     p.start()
#     print('zhu')




