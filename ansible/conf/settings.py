import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
server_ini = os.path.join(BASE_DIR,'conf','server.ini')

print(BASE_DIR)