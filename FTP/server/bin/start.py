#_*_coding:utf-8_*_



import os
import sys

BASE_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from src import server
import socketserver




if __name__ == '__main__':
    print("----------欢迎使用ftp----------""\n")
    ftpserver = socketserver.ThreadingTCPServer(('127.0.0.1', 8083), server.FtpServer)
    ftpserver.serve_forever()
    server.register()


