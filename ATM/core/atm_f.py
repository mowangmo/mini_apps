import logging

from ATM.config.settings import *
from ATM.lib.common_f import funcs, confirm
from ATM.core.db_f import sql_distribute
from ATM.core.login_f import auth

logger = logging.getLogger(__name__)


@auth(egine="file")
def atm():
    """
    主界面输入编号进入不同的功能
    :return:
    """
    func = {
        "0": {"name": "账户信息", "func": user_account},
        "1": {"name": "取现", "func": encashment},
        "2": {"name": "还款", "func": repayment},
        "3": {"name": "转账", "func": transfer},
        "4": {"name": "账单", "func": user_bill},
        "5": {"name": "退出", "func": "5"}
    }
    return funcs(func)


def user_account(loginname):
    """
    用户账户功能展示账户信息
    :return:
    """
    print("用户账户功能展示账户信息")
    sql = "select name,money,age,phone,date from %s where login = %s" % (db_emp, loginname)
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
        sql = "select name,money,age,phone,date from %s where login = %s" % (db_emp, loginname)
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
                    sql_list = []
                    sql_list.append("update %s set money = %.2f where login = %s" % (db_emp, money, loginname))
                    sql_list.append("insert into %s values (%s,%s,%.2f,%s,%s)" % (db_bill, loginname, '提现', amt, 0,
                                                                                  time.strftime("%Y-%m-%d",
                                                                                                time.localtime())))
                    sql_list.append(
                        "insert into %s values (%s,%s,%.2f,%s,%s)" % (db_bill, loginname, '手续费', amt * 0.05, 0,
                                                                      time.strftime("%Y-%m-%d", time.localtime())))
                    sql_distribute(sql_list)
                    logger.info("%s执行提现操作，共提取%.2f元现金" % (user_value['name'], amt))
                    print("取现成功，账户额度为：%.2f ！提现额度为：%.2f，其中手续费为：%.2f" % (money, amt, amt * 0.05))
                    if confirm("提现"):
                        continue
                    else:
                        return
                elif inp.upper() == 'N':
                    logger.info("用户%s取消提现" % user_value['name'])
                    if confirm("返回上一层"):
                        return
                    else:
                        continue
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
    sql = "select name,limit,money from %s where login = %s" % (db_emp, loginname)
    user_value = sql_distribute(sql)[0]
    pay = user_bill(loginname)
    while True:
        if float(user_value['limit']) != float(user_value['money']) and pay['sum_num'] == 0:
            print("未还款金额为%.2f" % (float(user_value['limit']) - float(user_value['money'])))
            tag = input("是否确认还款？“Y”是，“N”否").strip()
            if tag.upper() == 'Y':
                sql_list = []
                sql_list.append(
                    "update %s set money = %.2f where login = %s" % (db_emp, float(user_value['limit']), loginname))
                sql_list.append("insert into %s values (%s,%s,%s,%s,%s)" % (
                    db_bill, loginname, '还款', (float(user_value['limit']) - float(user_value['money'])), 0,
                    time.strftime("%Y-%m-%d", time.localtime())))
                sql_distribute(sql_list)
                logger.info("用户%s还款成功，还款金额为：%s" % (user_value['name'],
                                                   (float(user_value['limit']) - float(user_value['money']))))
                return print("还款成功")
            elif tag.upper() == 'N':
                if confirm("返回上一层"):
                    return
                else:
                    continue
            else:
                logger.error("输入有误")
                print("输入错误请重新输入")
        elif pay['sum_num'] == 0:
            return print("本月无需还款")
        else:
            print("需还款的总金额为%s" % pay['sum_num'])
            tag = input("是否确认还款？“Y”是，“N”否").strip()
            if tag.upper() == 'Y':
                money = pay['sum_num'] + float(user_value['money'])
                sql_list = []
                sql_list.append("update %s set money = %.2f where login = %s" % (db_emp, money, loginname))
                sql_list.append("insert into %s values (%s,%s,%s,%s,%s)" % (db_bill, loginname, '还款', pay['sum_num'], 0,
                                                                            time.strftime("%Y-%m-%d",
                                                                                          time.localtime())))
                sql_distribute(sql_list)
                for key in pay['id']:
                    sql = "update %s set type = 1 where id = %s" % (db_bill, key)
                    sql_distribute(sql)
                logger.info("用户%s还款成功，还款金额为：%s" % (user_value['name'], money))
                return print("还款成功")
            elif tag.upper() == 'N':
                if confirm("返回上一层"):
                    return
                else:
                    continue
            else:
                logger.error("输入有误")
                print("输入错误请重新输入")


def transfer(loginname):
    """
    转账功能
    :return:
    """
    while True:
        sql = "select name,limit,money from %s where login = %s" % (db_emp, loginname)
        out_user = sql_distribute(sql)[0]
        print("姓名：%s，账户额度：%s，可用额度：%s" % (out_user['name'], out_user['limit'], out_user['money']))
        in_user = input("请输入转账的账户：").strip()
        logger.info("登录用户%s，输入被转账用户%s讯息" % (loginname, in_user))
        sql = "select name,money from %s where login = %s" % (db_emp, in_user)
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
                        sql_list = []
                        sql_list.append("update %s set money = %.2f where login = %s" % (db_emp, in_amt, in_user))
                        out_amt = float(out_user['money']) - float(amt)
                        sql_list.append("update %s set money = %.2f where login = %s" % (db_emp, out_amt, loginname))
                        sql_list.append("insert into %s values (%s,%s,%s,%s,%s)" % (db_bill, loginname, '转账', amt, 0,
                                                                                    time.strftime("%Y-%m-%d",
                                                                                                  time.localtime())))
                        sql_distribute(sql_list)
                        logger.info("%s执行转账操作，转正金额为：%s元，被转账用户为：%s" % (out_user['name'], amt, in_user_value['name']))
                        print("转账成功")
                        if confirm("转账"):
                            break
                        else:
                            return
                    elif tag.upper() == 'N':
                        logger.info("用户%s取消转账" % out_user['name'])
                        if confirm("返回上一层"):
                            return
                        else:
                            continue
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
    start_time = time.mktime(
        time.strptime(("%s-%s-%s" % (localtime.tm_year, int(localtime.tm_mon) - 1, 23)), "%Y-%m-%d"))
    end_time = time.mktime(time.strptime(("%s-%s-%s" % (localtime.tm_year, int(localtime.tm_mon), 22)), "%Y-%m-%d"))
    sql = "select id,describe,amt,type,date from %s where login = %s and amt != 0.0 and type != 1 and describe != %s" % (
        db_bill, loginname, '还款')
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
    users_sql = "select login from %s" % db_emp
    users = sql_distribute(users_sql)
    localtime = time.localtime(time.time())
    end_time = time.mktime(time.strptime(("%s-%s-%s" % (localtime.tm_year, int(localtime.tm_mon) - 1, 22)), "%Y-%m-%d"))
    for v in users:
        loginname = v['login']
        sql = "select amt,date from %s where login = %s and type != 1 and describe != %s and describe != %s" % (
            db_bill, loginname, '还款', '利息')
        s1 = sql_distribute(sql)
        if s1[0] is not None:
            select_interest(localtime, loginname, end_time)
        else:
            continue


def select_interest(localtime, loginname, end_time, count=0):
    time_now = "%s-%s-%s" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday - count)
    sql = "select date from %s where login = %s and describe = %s and date like %s" % (db_bill, loginname, '利息',
                                                                                       time_now)
    stop_time = "%s-%s-%s" % (localtime.tm_year, localtime.tm_mon, 10)
    if sql_distribute(sql)[0] is None and time_now != stop_time:
        count += 1
        count = select_interest(localtime, loginname, end_time, count)
    if count != 0:
        count -= 1
        time_now = "%s-%s-%s" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday - count)
        join_interest(loginname, time_now, end_time)
    return count


def join_interest(loginname, time_now, end_time):
    sql = "select amt,date from %s where login = %s and type != 1 and describe != %s and describe != %s" % (
        db_bill, loginname, '还款', '利息')
    sql_value = sql_distribute(sql)
    if sql_value[0] is None:
        return
    value = {"sum_num": 0}
    for key in sql_value:
        key['date'] = time.mktime(time.strptime(key['date'][0:len(key['date']) - 1], "%Y-%m-%d"))
        if key['date'] <= end_time:
            value['sum_num'] += float(key['amt'])
    interest_num = round(value['sum_num'] * 0.0005, 2)
    if interest_num == 0.0:
        return
    sql1 = "insert into %s values (%s,%s,%s,%s,%s)" % (db_bill, loginname, '利息', interest_num, 0, time_now)
    return sql_distribute(sql1)