import time
from ATM.conf.settings import *
from ATM.lib.other_function import confirm, select_user_value, funcs
from ATM.lib.login_function import auth
db_inp = {"1": sql_emp, "2": sql_admin}


@auth(egine="mysql")
def backstage():
    """
    包括添加账户、用户额度，冻结账户等
    :return:
    """
    func = {
        "0": {"name": "添加账户", "function": useradd},
        "1": {"name": "修改账户", "function": usermod},
        "2": {"name": "删除账户", "function": userdel},
        "3": {"name": "额度修改", "function": quotamod},
        "4": {"name": "冻结账户", "function": userfreeze},
        "5": {"name": "退出", "function": "5"}
    }
    return funcs(func)


def useradd(loginname):
    """
    添加账户功能
    :return:
    """
    while True:
        print("登录用户[%s]" % loginname)
        inp = input("确认添加用户还是管理员？1：用户，2：管理员，3：退出").strip()
        if inp == '1':
            user_id = input("请输入添加用户的登录名称。").strip()
            user_pwd = input("请输入添加用户的密码。").strip()
            user_name = input("请输入添加用户的姓名。").strip()
            user_limit = input("请输入添加用户的账单额度。").strip()
            user_age = input("请输入添加用户的年龄。").strip()
            user_phone = input("请输入添加用户的电话。").strip()
            print("所添加的用户信息为：")
            print("登录名：%s，密码：%s，姓名：%s，额度：%s，年龄：%s，电话：%s" % (
                user_id, user_pwd, user_name, user_limit, user_age, user_phone))
            sql = "insert into %s values (%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (
                sql_emp, user_id, user_pwd, user_name, user_limit, user_limit, user_age, user_phone, 0,
                time.strftime("%Y-%m-%d", time.localtime()))
            if confirm('添加该用户', sql):
                continue
        elif inp == '2':
            admin_id = input("请输入添加用户的登录名称。").strip()
            admin_pwd = input("请输入添加用户的密码。").strip()
            admin_name = input("请输入添加用户的姓名。").strip()
            admin_phone = input("请输入添加用户的电话。").strip()
            print("所添加的用户信息为：")
            print("登录名：%s，密码：%s，姓名：%s，电话：%s" % (
                admin_id, admin_pwd, admin_name, admin_phone))
            sql = "insert into %s values (%s,%s,%s,%s,%s,%s)" % (
                sql_admin, admin_id, admin_pwd, admin_name, admin_phone, 0,
                time.strftime("%Y-%m-%d", time.localtime()))
            if confirm('添加该管理员', sql):
                continue
        elif inp == '3':
            return
        else:
            print("输入错误请重新输入")


def usermod(loginname):
    """
    修改账户功能
    :return:
    """
    while True:
        print("登录用户[%s]" % loginname)
        inp = input("请输入修改的用户类型？1：用户，2：管理员，3：退出").strip()
        if inp in db_inp and inp != '3':
            user_id = input("请输入要修改的账户登录名").strip()
            user_value = select_user_value(db_inp[inp], user_id)
            if isinstance(user_value, bool): continue
            while True:
                key = input("请输入需要修改名称信息：登录名称：login，密码：pwd，用户姓名：name，年龄：ag  e，联系方式：phone。")
                if key in user_value:
                    value = input("请输入需要修改的内容")
                    sql = "update %s set %s = %s where login = %s" % (db_inp[inp], key, value, user_id)
                    if confirm('修改', sql):
                        break
                else:
                    print("输入错误请重新输入")
        elif inp == '3':
            return
        else:
            print("输入错误请重新输入")


def userdel(loginname):
    """
    删除账户功能
    :return:
    """
    while True:
        print("登录用户[%s]" % loginname)
        inp = input("请输入删除的用户类型？1：用户，2：管理员，3：退出").strip()
        if inp in db_inp and inp != '3':
            user_id = input("请输入要删除的账户登录名").strip()
            user_value = select_user_value(db_inp[inp], user_id)
            if isinstance(user_value, bool): continue
            sql = "delete from %s where login = %s" % (db_inp[inp], user_id)
            if confirm('删除', sql):
                continue
        elif inp == '3':
            return
        else:
            print("输入错误请重新输入")


def userfreeze(loginname):
    """
    冻结账户功能
    :return:
    """

    while True:
        print("登录用户[%s]" % loginname)
        inp = input("请输入冻结的用户类型？1：用户，2：管理员，3：退出").strip()
        if inp in db_inp and inp != '3':
            user_id = input("请输入要冻结的账户登录名").strip()
            user_value = select_user_value(db_inp[inp], user_id)
            print(user_value)
            if isinstance(user_value, bool): continue
            sql = "update %s set count = %s where login = %s" % (db_inp[inp], 3, user_id)
            if confirm('冻结', sql):
                continue
        elif inp == '3':
            return
        else:
            print("输入错误请重新输入")


def quotamod(loginname):
    """
    额度修改功能
    :return:
    """
    while True:
        print("登录用户[%s]" % loginname)
        user_id = input("请输入要修改额度的账户登录名，输入‘Q’退出").strip()
        if user_id.upper() != 'Q':
            user_value = select_user_value(sql_emp, user_id)
            if isinstance(user_value, bool): continue
            while True:
                print("当前额度为：%s" % user_value['limit'])
                inp = input("需要修改的额度").strip()
                if inp.isdigit():
                    break
                else:
                    print("请输入数字")
            sql = "update %s set limit = %s where login = %s" % (sql_emp, inp, user_id)
            if confirm('修改额度', sql):
                continue
        elif user_id.upper() == 'Q':
            return
        else:
            print("输入错误请重新输入")

if __name__ == '__main__':
    backstage()