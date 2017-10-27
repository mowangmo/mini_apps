import re
exp = '-1-3*(-2+3)'
exp = [i for i in re.split('(\-\d+\.*\d*)', exp) if i]  # 以负数为分隔符，进行切分；去空格
expression_l = []
print('exp :' ,exp)
for i in exp:
    if len(expression_l)==0 and re.search('^\-',i):
        expression_l.append(i)
        print('e_l ==0 :' ,expression_l)

    elif re.search('[-+*/(]$]',expression_l[-1]):
        expression_l.append(i)
        print('e_l elif :', expression_l)
    else:
        l = re.split('([-+*/()])',i)
        print('i:' ,i)
        print('l :' ,l)
        expression_l+=l
        print('e_l else :', expression_l)
expression_l = [ i for i in expression_l if i ]
print('e_l :' ,expression_l)


c = '-3'
d = re.split('([-+*/()])',c)
print(d)
