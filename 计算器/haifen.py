#_*_coding:utf-8_*_
import re
def is_symbol(element):
    res=False
    symbol=['+','-','*','/','(',')']
    if element in symbol:
        res=True
    return res

def priority(top_sym,wait_sym):
    # print('from the priotry : ',top_sym,wait_sym)
    level1=['+','-']
    level2=['*','/']
    level3=['(']
    level4=[')']
    #运算符栈栈顶元素为+-
    if top_sym in level1:
        # if wait_sym in level1:
        #     return '>'
        # elif wait_sym in level2: # top_sym='-' wait_sym='*'
        #     return '<'
        # elif wait_sym in level3: # top_sym='-' wait_sym='('
        #     return '<'
        # elif wait_sym in level4: # top_sym='-' wait_sym=')'
        #     return '>'
        # else:
        #     return '>'
        if wait_sym in level2 or wait_sym in level3:
            return '<'
        else:
            return '>'

    #运算符栈栈顶元素为*/
    elif top_sym in level2:
        # if wait_sym in level1:# top_sym='*' wait_sym='+'
        #     return '>'
        # elif wait_sym in level2:# top_sym='*' wait_sym='*'
        #     return '>'
        # elif wait_sym in level3:# top_sym='*' wait_sym='('
        #     return '<'
        # elif wait_sym in level4:# top_sym='*' wait_sym=')'
        #     return '>'
        # else:
        #     return '>'
        if wait_sym in level3:
            return '<'
        else:
            return '>'

    #运算符栈栈顶元素为(
    elif top_sym in level3:
        if wait_sym in level4: #右括号)碰到了(,那么左括号应该弹出栈
            return '='
        else:
            return '<'  #只要栈顶元素为(,等待入栈的元素都应该无条件入栈
    #运算符栈栈顶元素为)

def calculate(num1,symbol,num2):
    res=0
    if symbol == '+':
        res=num1+num2
    elif symbol == '-':
        res=num1-num2
    elif symbol == '*':
        res=num1*num2
    elif symbol == '/':
        res=num1/num2
    print('from calculate res is [%s|%s|%s] %s' %(num1,symbol,num2,res))
    return res

def init_action(expression):
    # print(expression)
    expression=re.sub(' ','',expression)
    # print(expression)
    # print(re.findall('(\-\d+\.*\d*)',expression))   #提取负数['-1', '-2', '-60', '-40', '-9', '-2', '-5', '-7', '-568', '-4', '-3', '-3']
    init_l=[i for i in re.split('(\-\d+\.*\d*)',expression) if i]   #以负数为分割，形成列表
    print('init_l--->',init_l)      # ['-1', '-2', '*((', '-60', '+30+(', '-40', '/5)*(', '-9', '-2', '*', '-5', '/30', '-7', '/3*99/4*2998+10/', '-568', '/14))-(', '-4', '*', '-3', ')/(16', '-3', '*2))+3']
    expression_l=[]     #定义一个空列表
    while True:     #死循环
        if len(init_l) == 0:break
        exp=init_l.pop(0)   #提取列表中的第一位
        print('exp==>',exp)     #exp==> -1  exp==> -2
        if len(expression_l) == 0 and re.search('^\-\d+\.*\d*$',exp):
            expression_l.append(exp)
            continue
        if len(expression_l) > 0:
            if re.search('[\+\-\*\/\(]$',expression_l[-1]):
                expression_l.append(exp)

                continue

        new_l=[i for i in re.split('([\+\-\*\/\(\)])',exp) if i]
        expression_l+=new_l     #列表相加
        # print(expression_l)
        print('e_l : %s  ' % expression_l)  #e_l : ['-1', '-', '2', '*', '(', '(', '-60', '+', '30', '+', '(', '-40', '/', '5', ')', '*', '(', '-9', '-', '2', '*', '-5', '/', '30', '-', '7'] 将所有字符拆分开了
    return expression_l

def main(expression_l):
    # print('from in the main',expression_l)
    number_stack=[]
    symbol_stack=[]
    for ele in expression_l:
        print('-'*20)
        print('数字栈',number_stack)
        print('运算符栈',symbol_stack)
        print('待入栈运算符',ele)

        ret=is_symbol(ele)
        if not ret:
            #压入数字栈
            ele=float(ele)
            number_stack.append(ele)
        else:
            #压入运算符栈
            while True:
                if len(symbol_stack) == 0:
                    symbol_stack.append(ele)
                    break
                res=priority(symbol_stack[-1],ele)

                if res == '<':
                    symbol_stack.append(ele)
                    break
                elif res == '=':
                    symbol_stack.pop()
                    break
                elif res == '>':
                    symbol=symbol_stack.pop()
                    num2=number_stack.pop()
                    num1=number_stack.pop()
                    number_stack.append(calculate(num1,symbol,num2))

    else:
        symbol=symbol_stack.pop()
        num2=number_stack.pop()
        num1=number_stack.pop()
        number_stack.append(calculate(num1,symbol,num2))

    return number_stack,symbol_stack

if __name__ == '__main__':
    expression='-1 - 2 *((-60+30+(-40/5)*(-9-2*-5/30-7/3*99/4*2998+10/-568/14))-(-4*-3)/(16-3*2))+3'
    # expression='1-2*((60+2*(-3-40.0/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
    # expression='(1-2*3)-1-2*((-60+30+(-40/5)*(-9-2*-5/30-7/3*99/4*2998+10*568/14))-(-4*-3)/(16-3*2))+3'
    # expression='-1 -3*( -2+3)'
    expression_l=init_action(expression)

    # print(expression_l)

    l=main(expression_l)
    # print('====>',l)
    print('最终结果是:%s' %l[0][0])