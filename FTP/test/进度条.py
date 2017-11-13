import sys
import time
total_size=10212
recv_size=0
def progress(percent,width=50):
    if percent > 1: #如果百分比大于1的话则取1
        percent=1
    show_str=('[%%-%ds]' %width) %(int(percent*width)*'#')
    #一共50个#，%d 无符号整型数,-代表左对齐，不换行输出，两个% % 代表一个单纯的%，对应的是后面的s，后面为控制#号的个数
    # print(show_str)  #[###############               ] show_str ，每次都输出一次
    print('\r%s %s%%' %(show_str,int(percent*100)),end='',file=sys.stdout,flush=True)
    #\r 代表调到行首的意思，\n为换行的意思，fiel代表输出到哪，flush=True代表无延迟，立马刷新。第二个%s是百分比
while recv_size < total_size:   #当接收的大小小于总大小时
    time.sleep(0.2) #1024
    recv_size+=1024     #每次接收1024
    percent=recv_size/total_size    #计算百分比 0.10027418723070897
    progress(percent,width=30)  #调用进度条函数，将百分比传进去