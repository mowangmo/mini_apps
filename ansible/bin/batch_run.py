#_*_coding:utf-8_*_
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
from lib import my_optparse
from src import my_batch
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor,Executor
from lib import my_ssh
import configparser
from conf import settings

if __name__ == '__main__':
    options = my_optparse.my_opt()  #对用户输入参数进行解析
    print('用户输入参数：',options)  #{'cmd': 'df -TH', 'host': 'b', 'group': 'a'}输入参数返回字典
    batch_obj = my_batch.Batch(options)  #调用主函数，生成一个对象，进行批量操作
    parse_ini_host_l,cmd = batch_obj.parse_ini()   #调用解析配置文件方法

    pool = ThreadPoolExecutor()  # 开启线程池
    pool_objs = []  # 接收多线程的返回结果

    config = configparser.ConfigParser()    #读取配置文件
    config.read(settings.server_ini)

    for h in parse_ini_host_l:
        hostname = config.get(h, 'hostname')      #将配置文件中的信息赋值
        port = config.get(h,'port')
        username = config.get(h,'username')
        password = config.get(h,'password')

        print('异步执行命令：',hostname,port,username,'password',cmd)
        pool_obj = pool.submit( my_ssh.Ssh_server(hostname, port,username, password).run_cmd,cmd)     #通过进程池的方式连接
        pool_objs.append(pool_obj)  # 将对象放到列表中，等待取结果
        pool_obj_close=pool.submit( my_ssh.Ssh_server(hostname, port,username, password).close,h)        #关闭连接

    pool.shutdown(wait=True)  # shutdown代表不允许再往进程池里提交任务,wait=True就是join的意思：等待任务都执行完毕

    print('\n','-----命令返回结果-----','\n')
    for obj in pool_objs:
        print(obj.result())






