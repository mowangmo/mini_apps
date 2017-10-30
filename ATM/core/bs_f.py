from ATM.config.settings import *
from ATM.lib.common_f import confirm, funcs
from ATM.core.login_f import auth
from ATM.core.db_f import sql_distribute

db_inp = {"1": db_emp, "2": db_bs}


@auth(egine="mysql")
def backstage():
    """
    包括添加账户、用户额度，冻结账户等
    :return:
    """
    func = {
        "0": {"name": "添加账户", "func": useradd},
        "1": {"name": "修改账户", "func": usermod},
        "2": {"name": "删除账户", "func": userdel},
        "3": {"name": "额度修改", "func": quotamod},
        "4": {"name": "冻结账户", "func": userfreeze},
        "5": {"name": "退出", "func": "5"}
    }
    return funcs(func)


def useradd(loginname):
    """
    添加账户功能
    :return:
    """

    while True:
        inp_role = {
            "1": {"登录名称": "", "密码": "", "姓名": "", "账单额度": "", "可用额度": "", "年龄": "", "电话": ""},
            "2": {"登录名称": "", "密码": "", "姓名": "", "电话": ""}
        }
        print("登录用户[%s]" % loginname)
        inp = input("确认添加用户还是管理员？1：用户，2：管理员，3：退出").strip()
        if inp in db_inp and inp in inp_role and inp != '3':
            value_str = ""
            for k in inp_role[inp].keys():
                if k == "可用额度":
                    inp_role[inp][k] = inp_role[inp]["账单额度"]
                    continue
                else:
                    inp_role[inp][k] = input("请输入添加信息的%s。" % k).strip()
            print("所添加的信息为：")
            for k, v in inp_role[inp].items():
                print("%s：%s" % (k, v))
                value_str += "%s," % v
            value_str = value_str[0:len(value_str) - 1]
            sql = "insert into %s values (%s,%s,%s)" % (db_inp[inp], value_str, 0,
                                                        time.strftime("%Y-%m-%d", time.localtime()))
            print(inp_role)
            if confirm('添加该信息'):
                sql_distribute(sql)
            else:
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
            user_value = select_user_value(db_emp, user_id)
            if isinstance(user_value, bool): continue
            while True:
                print("当前额度为：%s" % user_value['limit'])
                inp = input("需要修改的额度").strip()
                if inp.isdigit():
                    break
                else:
                    print("请输入数字")
            sql = "update %s set limit = %s where login = %s" % (db_emp, inp, user_id)
            if confirm('修改额度', sql):
                continue
        elif user_id.upper() == 'Q':
            return
        else:
            print("输入错误请重新输入")


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
