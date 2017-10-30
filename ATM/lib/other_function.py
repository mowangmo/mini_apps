import time
import logging
from ATM.bin.start import current_status
from ATM.lib.sql_function import sql_distribute
from ATM.conf.settings import *
logger = logging.getLogger(__name__)


def funcs(func):
    while True:
        printlol(func)
        inp = input("请输入编号：")
        if inp in func and func[inp]["name"] != '退出':
            logger.warning("调用%s功能函数：%s" % (func[inp]["name"], func[inp]["function"].__name__))
            func[inp]["function"](current_status['user'])
            continue
        elif func[inp]["name"] == '退出':
            current_status['login_starus'] = False
            logger.info("执行退出功能，用户：%s 登录状态变为：%s" %(current_status['user'], current_status['login_starus']))
            return print("返回上一级菜单")
        else:
            print("输入错误请重新输入")


def printlol(func):
    """
    打印菜单功能字典嵌套
    :param func:
    :return:
    """
    print("============================")
    for print_value in func.items():
        if print_value[1].get("function"):
            print("ID：{},名称：{}".format(print_value[0], print_value[1]["name"]))
        elif print_value[1].get("price"):
            print("商品ID为:{},商品名为:{},价格为：{}".format(print_value[0], print_value[1]["name"],
                                                   print_value[1]["price"]))
        elif print_value[1].get("sum_amt"):
            print("商品名为:{},商品单价:{},商品总价：{}".format(print_value[0], print_value[1]["num"],
                                                   print_value[1]["sum_amt"]))
        else:
            pass
    print("============================")
    return


def select_interest(localtime, loginname, end_time, x=0):
    time_now = "%s-%s-%s" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday - x)
    sql = "select date from %s where login = %s and describe = %s and date like %s" % (sql_bill, loginname, '利息',
                                                                                       time_now)
    stop_time = "%s-%s-%s" % (localtime.tm_year, localtime.tm_mon, 10)
    if sql_distribute(sql)[0] is None and time_now != stop_time:
        x += 1
        x = select_interest(localtime, loginname, end_time, x)
    if x != 0:
        x -= 1
        time_now = "%s-%s-%s" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday - x)
        join_interest(loginname, time_now, end_time)
    return x


def join_interest(loginname, time_now, end_time):
    sql = "select amt,date from %s where login = %s and type != 1 and describe != %s and describe != %s" % (
        sql_bill, loginname, '还款', '利息')
    ss = sql_distribute(sql)
    if ss[0] is None:
        return
    value = {"sum_num": 0}
    for key in ss:
        key['date'] = time.mktime(time.strptime(key['date'][0:len(key['date']) - 1], "%Y-%m-%d"))
        if key['date'] <= end_time:
            value['sum_num'] += float(key['amt'])
    interest_num = round(value['sum_num'] * 0.0005, 2)
    sql1 = "insert into %s values (%s,%s,%s,%s,%s)" % (sql_bill, loginname, '利息', interest_num, 0, time_now)
    return sql_distribute(sql1)


def userprint(user_value):
    if not user_value:
        print("该用户不存在")
        return False
    if 'age' in user_value:
        print("================用户信息===================")
        print("登录名称：{}，密码：{}，注册时间：{}".format(user_value['login'], user_value['pwd'], user_value['date']), end='')
        print("用户姓名：{}，年龄：{}，联系方式：{}".format(user_value['name'], user_value['age'], user_value['phone']))
        print("==========================================")
    else:
        print("================管理员信息===================")
        print("登录名称：{}，密码：{}，注册时间：{}".format(user_value['login'], user_value['pwd'], user_value['date']), end='')
        print("用户姓名：{}，联系方式：{}".format(user_value['name'], user_value['phone']))
        print("==========================================")
    return


def select_user_value(db, user_id):
    sql = "select * from %s where login = %s" % (db, user_id)
    user_value = sql_distribute(sql)[0]
    if not isinstance(userprint(user_value), bool):
        return user_value
    else:
        return False


def confirm(func, sql):
    while True:
        tag = input("是否%s（是Y/否N）" % func).strip()
        if tag.upper() == 'Y':
            sql_distribute(sql)
            return True
        elif tag.upper() == 'N':
            print("取消修改")
            return True
        else:
            print("输入错误")
            continue