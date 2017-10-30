import time
from ATM.lib.common_f import printlol
from ATM.config.settings import *
from ATM.core.db_f import sql_distribute
from ATM.core.login_f import auth
from ATM.core.atm_f import repayment


def shopping():
    """
    购物车
    :return:
    """
    commodity_dic = {
        "1": {"name": 'apple', "price": 10},
        "2": {"name": 'tesla', "price": 100000},
        "3": {"name": 'mac', "price": 3000},
        "4": {"name": 'lenovo', "price": 30000},
        "5": {"name": 'chicken', "price": 10}
    }
    shopping_cart = {}
    shopping_all_amt = 0
    while True:
        for shopping_cart_info in commodity_dic.items():
            print("商品ID为:{},商品名为:{},价格为：{}".format(shopping_cart_info[0], shopping_cart_info[1]["name"],
                                                   shopping_cart_info[1]["price"]))
        commodity_id = input("请输入购买商品的ID：").strip()
        if commodity_id not in commodity_dic:
            print("您输入的信息有误，请重新输入！")
            continue
        shopping_tag = True
        while shopping_tag:
            commodity_mun = input("请输入购买的数量：").strip()
            if commodity_mun.isdigit():
                commodity_mun = int(commodity_mun)
                print("‘%s’成功添加到购物车,数量为：%s" % (commodity_dic[commodity_id]["name"], commodity_mun))
                if commodity_dic[commodity_id]["name"] in shopping_cart:
                    shopping_cart[commodity_dic[commodity_id]["name"]]["num"] += commodity_mun
                    shopping_cart[commodity_dic[commodity_id]["name"]]["sum_amt"] = \
                        shopping_cart[commodity_dic[commodity_id]["name"]]["num"] * commodity_dic[commodity_id]["price"]
                    shopping_cart[commodity_dic[commodity_id]["name"]]["pay_date"] = \
                        time.strftime("%Y-%m-%d", time.localtime())
                else:
                    shopping_cart.update({commodity_dic[commodity_id]["name"]: {
                        'num': commodity_mun, 'sum_amt': commodity_dic[commodity_id]["price"] * commodity_mun,
                        'pay_date': time.strftime("%Y-%m-%d", time.localtime())}})
                printlol(shopping_cart)
                while shopping_tag:
                    shopping_out = input("是否继续选择商品？（是Y/否N）").upper()
                    if shopping_out == "N":
                        for key in shopping_cart:
                            shopping_all_amt += shopping_cart[key]["sum_amt"]
                        if checkout(shopping_all_amt):
                            for key in shopping_cart:
                                sql = "insert into %s values (%s,%s,%s,%s,%s)" % (
                                    db_pay, current_status['user'], key, shopping_cart[key]['num'],
                                    shopping_cart[key]['sum_amt'], shopping_cart[key]['pay_date'])
                                sql_distribute(sql)
                                shopping_cart = {}
                        current_status['login_starus'] = False
                        return
                    elif shopping_out == "Y":
                        shopping_tag = False
                    else:
                        print("输入错误请重新输入")
            else:
                print("请输入数字！")


@auth(egine="file")
def checkout(money):
    """
    结账功能
    :return:
    """
    loginname = current_status['user']
    sql = "select money,limit from %s where login = %s" % (db_emp, loginname)
    user_money = sql_distribute(sql)[0]
    user_money['money'] = float(user_money['money'])
    while True:
        if money > float(user_money['limit']):
            print("商品金额大于卡片限额，请联系银行调整额度后在购买！")
            return False
        elif money > user_money['money']:
            print("信用卡已被刷爆请还款后再购买")
            repayment(current_status['user'])
            continue
        elif money <= user_money['money']:
            inp = input("刷卡确认（是Y/否N）").upper()
            if inp == "Y":
                user_money['money'] -= money
                print("刷卡成功消费金额为：%s，可透支额度为：%.2f" % (money, user_money['money']))
                sql_list = []
                sql_list.append("update %s set money = %.2f where login = %s" % (db_emp, user_money['money'], loginname))
                sql_list.append("insert into %s values (%s,%s,%s,%s,%s)" % (db_bill, loginname, '消费', money, 0,
                                                                            time.strftime("%Y-%m-%d",
                                                                                          time.localtime())))
                sql_distribute(sql_list)
                return True
            elif inp == "N":
                print("取消购买")
                return False
            else:
                print("输入错误请重新输入")
        else:
            print("未知错误")
            return False
