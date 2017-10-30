import os

config_path = r'%s\%s' % (os.path.dirname(os.path.abspath(__file__)), 'config.ini')
user_timeout = 10
user_db_path = r'%s\%s' % (os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db')
sql_emp = 'db.emp'
sql_pay = 'db.pay'
sql_bill = 'db.bill'
sql_admin = 'db.admin'