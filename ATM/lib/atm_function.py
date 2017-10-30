import time
import logging

from ATM.conf.settings import *
from ATM.lib.other_function import select_interest, funcs
from ATM.lib.sql_function import sql_distribute
from ATM.lib.login_function import auth
logger = logging.getLogger(__name__)


@auth(egine="file")
def distribute():
    """
    主界面输入编号进入不同的功能
    :return:
    """
    func = {
        "0": {"name": "账户信息", "function": user_account},
        "1": {"name": "取现", "function": encashment},
        "2": {"name": "还款", "function": repayment},
        "3": {"name": "转账", "function": transfer_accounts},
        "4": {"name": "账单", "function": user_bill},
        "5": {"name": "退出", "function": "5"}
    }
    return funcs(func)


def user_account(loginname):
    """
    用户账户功能展示账户信息
    :return:
    """
    print("用户账户功能展示账户信息")
    sql = "select name,money,age,phone,date from %s where login = %s" % (sql_emp, loginname)
    ss = sql_distribute(sql)[0]
    logger.info("用户信息输出")
    print("==========================================")
    print("用户姓名：{}，年龄：{}，联系方式：{}".format(ss['name'], ss['age'], ss['phone']))
    print("账户余额：{}，注册时间：{}".format(ss['money'], ss['date']), end='')
    print("==========================================")
    return


def encashment(loginname):
    """
    取现功能
    :return:
    """
    print("取现功能")
    print("************************重要的事情说三遍**************************")
    print("**********提现会手续5%的手续费，费用会从账户中扣除**********")
    print("**********提现会手续5%的手续费，费用会从账户中扣除**********")
    print("**********提现会手续5%的手续费，费用会从账户中扣除**********")
    print("*********************************************************************")
    while True:
        sql = "select name,money,age,phone,date from %s where login = %s" % (sql_emp, loginname)
        user_value = sql_distribute(sql)[0]
        user_value['money'] = float(user_value['money'])
        cash = user_value['money'] - (user_value['money'] * 0.05)
        print("账户可透支额度%.2f，最大提现额度为%.2f" % (user_value['money'], cash))
        amt = input("请输入提现的金额：").strip()
        if amt.isdigit():
            amt = float(amt)
            logger.info("用户输入金额：%s" % amt)
            if amt > cash:
                logger.error("用户输入金额大于可提现额度")
                print("金额大于可提现额度")
                continue
            elif amt <= cash:
                money = user_value['money'] - (amt + (amt * 0.05))
                print("提现额度为：%s，其中手续费为：%s" % (amt, amt * 0.05))
                inp = input("是否确认取现？“Y”是，“N”否").strip()
                if inp.upper() == 'Y':
                    sql = "update %s set money = %.2f where login = %s" % (sql_emp, money, loginname)
                    sql_distribute(sql)
                    sql1 = "insert into %s values (%s,%s,%.2f,%s,%s)" % (sql_bill, loginname, '提现', amt, 0,
                                                                         time.strftime("%Y-%m-%d", time.localtime()))
                    sql_distribute(sql1)
                    sql2 = "insert into %s values (%s,%s,%.2f,%s,%s)" % (sql_bill, loginname, '手续费', amt * 0.05, 0,
                                                                         time.strftime("%Y-%m-%d", time.localtime()))
                    sql_distribute(sql2)
                    logger.info("%s执行提现操作，共提取%.2f元现金" % (user_value['name'], amt))
                    print("取现成功，账户额度为：%.2f ！提现额度为：%.2f，其中手续费为：%.2f" % (money, amt, amt * 0.05))
                    inp = input("是否继续提现？“Y”继续，“N”退出").strip()
                    if inp.upper() == 'Y':
                        continue
                    elif inp.upper() == 'N':
                        logger.warning("返回调用位置")
                        return
                    else:
                        logger.error("输入有误")
                        print("输入错误请重新输入")
                elif inp.upper() == 'N':
                    inp = input("是否返回上一层？“Y”返回上一层，“N”继续提现操作").strip()
                    logger.info("用户%s取消提现" % user_value['name'])
                    if inp.upper() == 'Y':
                        logger.warning("返回调用位置")
                        return
                    elif inp.upper() == 'N':
                        continue
                    else:
                        logger.error("输入有误")
                        print("输入错误请重新输入")
                else:
                    logger.error("输入有误")
                    print("输入错误请重新输入")
            else:
                print("未知错误")
        else:
            logger.error("输入有误")
            print("请输入数字")


def repayment(loginname):
    """
    还款功能
    :return:
    """
    sql = "select name,limit,money from %s where login = %s" % (sql_emp, loginname)
    user_value = sql_distribute(sql)[0]
    pay = user_bill(loginname)
    while True:
        if float(user_value['limit']) != float(user_value['money']) and pay['sum_num'] == 0:
            print("未还款金额为%.2f" % (float(user_value['limit']) - float(user_value['money'])))
            tag = input("是否确认还款？“Y”是，“N”否").strip()
            if tag.upper() == 'Y':
                sql = "update %s set money = %.2f where login = %s" % (sql_emp, float(user_value['limit']), loginname)
                sql_distribute(sql)
                sql1 = "insert into %s values (%s,%s,%s,%s,%s)" % (
                    sql_bill, loginname, '还款', (float(user_value['limit']) - float(user_value['money'])), 0,
                    time.strftime("%Y-%m-%d", time.localtime()))
                sql_distribute(sql1)
                logger.info("用户%s还款成功，还款金额为：%s" % (user_value['name'],
                                                   (float(user_value['limit']) - float(user_value['money']))))
                return print("还款成功")
            elif tag.upper() == 'N':
                inp = input("是否返回上一层？“Y”返回上一层，“N”继续还款操作").strip()
                if inp.upper() == 'Y':
                    logger.warning("返回调用位置")
                    return
                elif inp.upper() == 'N':
                    continue
                else:
                    logger.error("输入有误")
                    print("输入错误请重新输入")
            else:
                logger.error("输入有误")
                print("输入错误请重新输入")
        elif pay['sum_num'] == 0:
            print("本月无需还款")
            return
        else:
            print("需还款的总金额为%s" % pay['sum_num'])
            tag = input("是否确认还款？“Y”是，“N”否").strip()
            if tag.upper() == 'Y':
                money = pay['sum_num'] + float(user_value['money'])
                sql = "update %s set money = %.2f where login = %s" % (sql_emp, money, loginname)
                sql_distribute(sql)
                for key in pay['id']:
                    sql = "update %s set type = 1 where id = %s" % (sql_bill, key)
                    sql_distribute(sql)
                sql1 = "insert into %s values (%s,%s,%s,%s,%s)" % (sql_bill, loginname, '还款', pay['sum_num'], 0,
                                                                   time.strftime("%Y-%m-%d", time.localtime()))
                sql_distribute(sql1)
                logger.info("用户%s还款成功，还款金额为：%s" % (user_value['name'], money))
                print("还款成功")
                return
            elif tag.upper() == 'N':
                inp = input("是否返回上一层？“Y”返回上一层，“N”继续还款操作").strip()
                if inp.upper() == 'Y':
                    logger.warning("返回调用位置")
                    return
                elif inp.upper() == 'N':
                    continue
                else:
                    logger.error("输入有误")
                    print("输入错误请重新输入")
            else:
                logger.error("输入有误")
                print("输入错误请重新输入")


def transfer_accounts(loginname):
    """
    转账功能
    :return:
    """
    while True:
        sql = "select name,limit,money from %s where login = %s" % (sql_emp, loginname)
        out_user = sql_distribute(sql)[0]
        print("姓名：%s，账户额度：%s，可用额度：%s" % (out_user['name'], out_user['limit'], out_user['money']))
        in_user = input("请输入转账的账户：").strip()
        logger.info("登录用户%s，输入被转账用户%s讯息" % (loginname, in_user))
        sql = "select name,money from %s where login = %s" % (sql_emp, in_user)
        in_user_value = sql_distribute(sql)[0]
        if in_user_value:
            while True:
                amt = input("请输入转账的金额，金额最大不能超过：%s" % out_user['money']).strip()
                if not amt.isdigit():
                    logger.error("用户输入不是数字")
                    print("请输入数字")
                    continue
                elif float(amt) < float(out_user['money']):
                    logger.info("用户输入金额：%s" % amt)
                    tag = input("是否确认转账给[%s]？转账金额为：%s。“Y”是，“N”否" % (in_user_value['name'], amt)).strip()
                    if tag.upper() == 'Y':
                        in_amt = float(amt) + float(in_user_value['money'])
                        sql = "update %s set money = %.2f where login = %s" % (sql_emp, in_amt, in_user)
                        sql_distribute(sql)
                        out_amt = float(out_user['money']) - float(amt)
                        sql1 = "update %s set money = %.2f where login = %s" % (sql_emp, out_amt, loginname)
                        sql_distribute(sql1)
                        sql2 = "insert into %s values (%s,%s,%s,%s,%s)" % (sql_bill, loginname, '转账', amt, 0,
                                                                           time.strftime("%Y-%m-%d", time.localtime()))
                        sql_distribute(sql2)
                        logger.info("%s执行转账操作，转正金额为：%s元，被转账用户为：%s" % (out_user['name'], amt, in_user_value['name']))
                        print("转账成功")
                        inp = input("是否继续转账？“Y”继续，“N”退出").strip()
                        if inp.upper() == 'Y':
                            break
                        elif inp.upper() == 'N':
                            logger.warning("返回调用位置")
                            return
                        else:
                            logger.error("输入有误")
                            print("输入错误请重新输入")
                    elif tag.upper() == 'N':
                        logger.info("用户%s取消转账" % out_user['name'])
                        inp = input("是否返回上一层？“Y”返回上一层，“N”继续转账操作").strip()
                        if inp.upper() == 'Y':
                            logger.warning("返回调用位置")
                            return
                        elif inp.upper() == 'N':
                            break
                        else:
                            logger.error("输入有误")
                            print("输入错误请重新输入")
                    else:
                        logger.error("输入有误")
                        print("输入错误请重新输入")
                else:
                    logger.error("用户输入的金额大于账户金额")
                    print("输入的金额大于账户金额")
        else:
            logger.error("输入用户名%s账户不存在" % in_user)
            print("账户不存在，请重新输入")


def user_bill(loginname):
    """
    账单功能
    :return:
    """

    localtime = time.localtime(time.time())
    start_time = "%s-%s-%s" % (localtime.tm_year, int(localtime.tm_mon) - 1, 23)
    end_time = "%s-%s-%s" % (localtime.tm_year, int(localtime.tm_mon), 22)
    start_time = time.mktime(time.strptime(start_time, "%Y-%m-%d"))
    end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d"))
    sql = "select id,describe,amt,type,date from %s where login = %s and amt != 0.0 and type != 1 and describe != %s" % (
        sql_bill, loginname, '还款')
    ss = sql_distribute(sql)
    value = {"sum_num": 0, "id": []}
    if ss:
        print("==============本月未还款账单==============")
        for key in ss:
            key['date'] = time.mktime(time.strptime(key['date'][0:len(key['date']) - 1], "%Y-%m-%d"))
            if start_time <= key['date'] <= end_time:
                print('类型：{}，金额：{}，时间：{}'.format(key['describe'], key['amt'], time.strftime("%Y-%m-%d",
                                                                                            time.localtime(
                                                                                                key['date']))))
                value['sum_num'] += float(key['amt'])
                value['id'].append(key['id'])
        print("==============早期未还款账单==============")
        for key in ss:
            if start_time > key['date']:
                print('类型：{}，金额：{}，时间：{}'.format(key['describe'], key['amt'], time.strftime("%Y-%m-%d",
                                                                                            time.localtime(
                                                                                                key['date']))))
                value['sum_num'] += float(key['amt'])
                value['id'].append(key['id'])
    return value


def interest():
    """
    利息功能
    :return:
    """
    users_sql = "select login from %s" % sql_emp
    users = sql_distribute(users_sql)
    localtime = time.localtime(time.time())
    end_time = "%s-%s-%s" % (localtime.tm_year, int(localtime.tm_mon) - 1, 22)
    end_time = time.mktime(time.strptime(end_time, "%Y-%m-%d"))
    for v in users:
        loginname = v['login']
        sql = "select amt,date from %s where login = %s and type != 1 and describe != %s and describe != %s" % (
            sql_bill, loginname, '还款', '利息')
        s1 = sql_distribute(sql)
        if s1[0] is not None:
            select_interest(localtime, loginname, end_time)
        else:
            continue


if __name__ == '__main__':
    distribute()
