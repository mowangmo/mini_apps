import logging
from ATM.lib.atm_function import distribute
from ATM.lib.bs_function import backstage
from ATM.lib.other_function import printlol
from ATM.lib.shop_function import shopping
logger = logging.getLogger(__name__)


def home():
    """
    主页
    :return:
    """
    func = {
        "0": {"name": "ATM", "function": distribute},
        "1": {"name": "购物车", "function": shopping},
        "2": {"name": "后台", "function": backstage},
        "3": {"name": "退出", "function": "3"}
    }
    while True:
        printlol(func)
        inp = input("请输入编号：")
        if inp in func and inp != '3':
            logger.warning("调用%s功能函数：%s" % (func[inp]["name"], func[inp]["function"].__name__))
            func[inp]["function"]()
        elif inp == '3':
            logger.info("退出程序")
            return print("退出程序")
        else:
            print("输入错误请重新输入")


if __name__ == '__main__':
    home()
