import os,sys
BASE_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from db import account_db

# print(account_db.all_account['admin'])