import os
import logging
from ATM.conf.settings import user_db_path
logger = logging.getLogger(__name__)
sql_dic = {"emp": "id,login,pwd,name,limit,money,age,phone,count,date",
           "pay": "id,login,commodity,num,total,date",
           "bill": "id,login,describe,amt,type,date",
           "admin": "id,login,pwd,name,phone,count,date"
           }


def sql_distribute(sql_str):
    func = {
        'select': select_module,
        'update': update_module,
        'insert': insert_module,
        'delete': delete_module
    }
    sql_list = sql_str.split()
    key = sql_list[0]
    if key in func:
        logger.warning("进入%s功能，调用%s子功能" % (sql_distribute.__name__, func[key].__name__))
        return func[key](sql_list)
    else:
        return print('输入错误')


def select_module(sql_str):
    """
    select id,name,age,phone from db1.emp where id>=10 and id < = 20 and name like 李
    :param sql_str:
    :return:
    """
    select_dict = {
        "select": [],
        "from": [],
        "where": [],
    }
    try:
        select_dict = sql_format(sql_str, select_dict)
        db = select_dict['from'][0].split('.')
        re_list = []
        if select_dict['select'][0] != "*":
            select_dict['select'] = select_dict['select'][0].split(',')
        with open("%s/%s" % (user_db_path, db[1]), 'r', encoding='utf-8') as f:
            for line in f:
                db_dict = dict(zip(sql_dic[db[1]].split(','), line.split(',')))
                if screen_print(select_dict['where'], db_dict):
                    select_value(select_dict, db_dict, re_list, line, db[1])
                elif len(select_dict['where']) == 0:
                    select_value(select_dict, db_dict, re_list, line, db[1])
            if len(re_list) == 0:
                re_list.append(None)
            f.close()
            return re_list
    except:
        print("语法有误请重新输入")
    return


def select_value(select_dict=None, db_dict=None, re_list=None, line=None, db=None):
    if select_dict['select'][0] != "*":
        v = {}
        for tag in select_dict['select']:
            if tag in db_dict:
                v.update({tag: db_dict[tag]})
            else:
                return print("查询条件不在字典中请重新输入")
        re_list.append(v)
    elif select_dict['select'][0] == "*":
        line = line.split(',')
        db_dict = dict(zip(sql_dic[db].split(','), line))
        re_list.append(db_dict)
    else:
        return True


def update_module(sql_str):
    """
    update db1.emp set name=sb,age=100 where id = 24
    :param sql_str:
    :return:
    """
    update_dict = {'update': [], 'set': [], "where": [], }
    try:
        update_dict = sql_format(sql_str, update_dict)
        db = update_dict['update'][0].split('.')
        update_dict['set'] = set_module(update_dict['set'], db[1])
        with open("%s/%s" % (user_db_path, db[1]), 'r', encoding='utf-8') as f, \
                open("%s/%s" % (user_db_path, db[1]) + '~', "w", encoding="utf-8") as write_f:
            write_str = ','
            for line in f:
                db_dict = dict(zip(sql_dic[db[1]].split(','), line.split(',')))
                if screen_print(update_dict['where'], db_dict):
                    lines = []
                    line = line.split(',')
                    for x in range(len(line)):
                        if x in update_dict['set']:
                            lines.append(update_dict['set'][x])
                        else:
                            lines.append(line[x])
                    write_f.write(write_str.join(lines))
                    print("数据修改成功")
                else:
                    write_f.write(line)
        os.remove("%s/%s" % (user_db_path, db[1]))
        os.rename("%s/%s" % (user_db_path, db[1]) + '~', "%s/%s" % (user_db_path, db[1]))
    except:
        print("语法有误请重新输入")
    return


def insert_module(sql_str):
    """
    insert into db1.emp (name,age,phone,job,date) values (阿萨德,26,18812312312,运营,2017-12-12)
    :param sql_str:
    :return:
    """
    insert_dict = {'into': [], "values": [], "insert_into": []}
    try:
        insert_dict = sql_format(sql_str, insert_dict)
        db = insert_dict['into'][0].split('.')
        if len(insert_dict['into']) > 1:
            insert_key = insert_into(insert_dict['into'][1])
        else:
            insert_key = sql_dic[db[1]].split(',')
        insert_values = insert_into(insert_dict['values'][0])
        insert_dict['insert_into'] = dict(zip(insert_key, insert_values))
        with open("%s/%s" % (user_db_path, db[1]), 'r', encoding='utf-8') as f, \
                open("%s/%s" % (user_db_path, db[1]) + '~', "w", encoding="utf-8") as write_f:
            write_str = ','
            count = 1
            lines = []
            for line in f:
                line = line.split(',')
                if 'phone' in insert_key:
                    if insert_dict['insert_into']['phone'] in line[3]:
                        f.close()
                        write_f.close()
                        os.remove("%s/%s" % (user_db_path, db[1]) + '~')
                        return print("唯一索引phone已存在")
                count = int(line[0]) + 1
                write_f.write(write_str.join(line))
            lines.append(str(count))
            for x in insert_values:
                lines.append(x)
            write_f.write(write_str.join(lines) + '\n')
            print("写入成功 %s" % lines)
        os.remove("%s/%s" % (user_db_path, db[1]))
        os.rename("%s/%s" % (user_db_path, db[1]) + '~',
                  "%s/%s" % (user_db_path, db[1]))
    except:
        print("语法有误请重新输入")
    return


def delete_module(sql_str):
    """
    delete from db1.emp where id = 26
    :param sql_str:
    :return:
    """
    delete_dict = {
        "from": [],
        "where": [],
    }
    try:
        delete_dict = sql_format(sql_str, delete_dict)
        db = delete_dict['from'][0].split('.')
        with open("%s/%s" % (user_db_path, db[1]), 'r', encoding='utf-8') as f, \
                open("%s/%s" % (user_db_path, db[1]) + '~', "w", encoding="utf-8") as write_f:
            write_str = ','
            for line in f:
                line = line.split(',')
                db_dict = dict(zip(sql_dic[db[1]].split(','), line))
                if screen_print(delete_dict['where'], db_dict):
                    print("已删除%s" % line)
                    continue
                write_f.write(write_str.join(line))
        os.remove("%s/%s" % (user_db_path, db[1]))
        os.rename("%s/%s" % (user_db_path, db[1]) + '~', "%s/%s" % (user_db_path, db[1]))
    except:
        print("语法有误请重新输入")
    return


def insert_into(value):
    if value.find('(') == -1 or value.find(')') == -1:
        return True
    del_space = ''
    value = del_space.join(value)
    value = value.split('(')[1].split(')')[0]
    return value.split(',')


def screen_print(where_key, db_dict):
    """
    可以对应where条件大于，小于，等于，大于等于，小于等于，like  查询列可以为空加入了select就可以筛出具体列来一次传一个字典类型的数据
    :param where_key: where条件 必须是[['列名','运算符','条件'],['列名','运算符','条件']，['列名','运算符','条件']]格式
    :param db_dict:读取内容必须是字典格式
    :return:然回list格式数据
    """
    tag = False
    for where_value in where_key:
        where_name, where_operator, where_num = where_value
        if db_dict[where_name].isdigit() and where_num.isdigit():
            db_dict[where_name] = int(db_dict[where_name])
            where_num = int(where_num)
        if where_operator == '>':
            if db_dict[where_name] > where_num:
                tag = True
            else:
                tag = False
            if not tag:
                break
        if where_operator == '<':
            if db_dict[where_name] < where_num:
                tag = True
            else:
                tag = False
            if not tag:
                break
        if where_operator == '<=':
            if db_dict[where_name] <= where_num:
                tag = True
            else:
                tag = False
            if not tag:
                break
        if where_operator == '>=':
            if db_dict[where_name] >= where_num:
                tag = True
            else:
                tag = False
            if not tag:
                break
        if where_operator == '=':
            if db_dict[where_name] == where_num:
                tag = True
            else:
                tag = False
            if not tag:
                break
        if where_operator == '!=':
            if db_dict[where_name] != where_num:
                tag = True
            else:
                tag = False
            if not tag:
                break
        if where_operator == 'like':
            if where_num in db_dict[where_name]:
                tag = True
            else:
                tag = False
    return tag


def where_module(where_value):
    where_value.append("and")
    key = 'and'
    where_char = ''
    where_list = []
    where_lists = []
    for i in where_value:
        if i != key:
            where_char += i
        else:
            where_list.append(where_char)
            where_char = ''
    for i in where_list:
        where_lists.append(operator_format(i))
    return where_lists


def operator_format(where_list):
    key = ['<', '>', '=', '!']
    where_char = ''
    operator = ''
    where_value = []
    tag = False
    if where_list.find('like') != -1:
        where_value.append(where_list.split('like')[0])
        where_value.append('like')
        where_value.append(where_list.split('like')[1])
        return where_value
    for x in where_list:
        if tag and x not in key:
            tag = False
            where_value.append(operator)
        if not tag and x not in key:
            where_char += x
        if x in key:
            if len(where_char) != 0:
                where_value.append(where_char)
            where_char = ''
            operator += x
            tag = True
    where_value.append(where_char)
    return where_value


def set_module(set_value, db):
    set_str = ''
    set_str = set_str.join(set_value)
    set_list = set_str.split(',')
    set_key = []
    for q in set_list:
        set_key.append(q.split('='))
    set_dict = dict(set_key)
    line = []
    for k in range(len(sql_dic[db].split(','))):
        line.append(k)
    line_num = dict(zip(sql_dic[db].split(','), line))
    set_dicts = {}
    for k in set_dict:
        if k in line_num:
            set_dicts.update({line_num[k]: set_dict[k]})
        else:
            pass
    return set_dicts


def sql_format(sql_str, sql_dict):
    tag = False
    for item in sql_str:
        if tag and item in sql_dict:
            tag = False
        if not tag and item in sql_dict:
            tag = True
            key = item
            continue
        if tag:
            sql_dict[key].append(item)
    if sql_dict.get('where'):
        sql_dict['where'] = where_module(sql_dict.get('where'))
    return sql_dict
