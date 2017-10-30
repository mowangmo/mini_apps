import logging
from ATM.config.settings import *
logger = logging.getLogger(__name__)


def funcs(func):
    while True:
        printlol(func)
        inp = input("请输入编号：")
        if inp in func and func[inp]["name"] != '退出':
            logger.warning("调用%s功能函数：%s" % (func[inp]["name"], func[inp]["func"].__name__))
            func[inp]["func"](current_status['user'])
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
        if print_value[1].get("func"):
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


def confirm(name):
    while True:
        tag = input("是否%s？“Y”是，“N”否" % name).strip()
        if tag.upper() == 'Y':
            return True
        elif tag.upper() == 'N':
            return False
        else:
            logger.error("输入有误")
            print("输入错误")