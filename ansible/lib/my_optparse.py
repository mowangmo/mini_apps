from optparse import OptionParser  
from optparse import OptionGroup

def my_opt():
    usage = "Usage: %prog -H h1 -g g1 --cmd 'df -TH'"
    parser = OptionParser(usage,version='%prog 1.0')
    parser.add_option('-H','--host',  action='store',help='参数后面接配置文件中hostname')
    parser.add_option('-c', '--cmd', action='store', help='参数后面接配置文件中系统命令')
    parser.add_option('-g', '--group', action='store', help='参数后面接配置文件中groupname')
    # group = OptionGroup(parser,'Group Options', '对组内用户起作用')
    # group.add_option('-g','--group',action='store_true',help='参数后面接配置文件中groupname')
    # parser.add_option_group(group)
    (options,args) = parser.parse_args()
    # print(options)
    # print(args)
    return options

