import logging
from ATM.core.db_f import sql_distribute
from functools import wraps
from ATM.config.settings import *
sql_db = {"file": db_emp, "mysql": db_bs}
logger = logging.getLogger(__name__)


def auth(egine='file'):
    """
    登录验证装饰器
    :param egine:
    :return:
    """

    def wreapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if current_status['user'] and current_status['login_starus']:
                res = func(*args, **kwargs)
                return res
            while True:
                name = input('username>>>:').strip()
                pwd = input('password>>>:').strip()
                sql = "select login,pwd,count from %s where login = %s" % (sql_db[egine], name)
                user_value = sql_distribute(sql)[0]
                if user_value is None:
                    logger.error("该账户不存在")
                    return print("该账户不存在")
                else:
                    user_value['count'] = int(user_value['count'])
                    if user_value.get('count') == 3:
                        logger.error("用户%s已被锁定，请联系客服！电话：XXXXXX" % name)
                        return print("用户%s已被锁定，请联系客服！电话：XXXXXX" % name)
                    elif user_value.get('login') == name and user_value.get('pwd') == pwd:
                        logger.info("登陆成功")
                        print('登陆成功')
                        current_status['user'] = name
                        current_status['login_starus'] = True
                        logger.info("用户【%s】处于登录状态 %s" % (current_status['user'], current_status['login_starus']))
                        res = func(*args, **kwargs)
                        return res
                    else:
                        user_value['count'] += 1
                        sql_update = "update %s set count = %s where login = %s" % (sql_db[egine], user_value['count'], name)
                        sql_distribute(sql_update)
                        logger.error("密码错误")
                        return print("密码错误")

        return inner

    return wreapper