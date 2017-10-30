import logging
from ATM.core.atm_f import atm
from ATM.core.bs_f import backstage
from ATM.lib.common_f import printlol
from ATM.core.shop_f import shopping
logger = logging.getLogger(__name__)


def main():
    """
    主页
    :return:
    """
    func = {
        "0": {"name": "ATM", "func": atm},
        "1": {"name": "购物车", "func": shopping},
        "2": {"name": "后台", "func": backstage},
        "3": {"name": "退出", "func": "3"}
    }
    while True:
        printlol(func)
        inp = input("请输入编号：")
        if inp in func and inp != '3':
            logger.warning("调用%s功能函数：%s" % (func[inp]["name"], func[inp]["func"].__name__))
            func[inp]["func"]()
        elif inp == '3':
            logger.info("退出程序")
            return print("退出程序")
        else:
            print("输入错误请重新输入")
