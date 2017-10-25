# -*- coding:utf-8 -*-
import re
import sys
import os
import json

# expression='1-2*((60+2*(-3-40.0/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
# expression='1 -2*10*(-9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
# content=re.search('\(([\-\+\*\/]*\d+\.?\d*)+\)',expression).group() #(-3-40.0/5)

def add_sub(bracket_content_after_md): #加减法
    print("处理加法运算: %s" %bracket_content_after_md)     #-3-8.0

    if re.search('(\d+\.?\d*)((\+\-)|(\-\-))(\d+\.?\d*)',bracket_content_after_md):     #提取+- -- 表达式
        first_add_sub = re.search('(\d+\.?\d*)((\+\-)|(\-\-))(\d+\.?\d*)', bracket_content_after_md).group()  # 提取加减法表达式
        # print(first_add_sub)    #60+-3818009.3809523815

        #加减为减，减减为加

        if re.search('\+',first_add_sub):   #如果有+ 那么就是+-，就可以转换为-
            first_add_sub = first_add_sub.replace('+','')
            # print(first_add_sub)

        elif re.search('\-\-',first_add_sub):
            first_add_sub = first_add_sub.replace('\-\-', '\-')

        first_add_sub_dig = re.split('\+|\-', first_add_sub)  # 将数字和+ - 号分离
        # print(first_add_sub_dig)    #['3', '8.0']

        if bracket_content_after_md[0] == '-':  # 加个负号判断
            first_dig = -float(first_add_sub_dig[0])  # 如果第一位是负号，这将第一个数字变为负数
            bracket_content_after_md = bracket_content_after_md[1:]  # 将这个负号去掉，因为已经变成负数了
            # print(bracket_content_after_md)
        else:
            first_dig = float(first_add_sub_dig[0])
        # print(first_dig)    #3.0
        second_dig = float(first_add_sub_dig[1])
        # print(second_dig)   #8.0
        first_add_sub_sym = re.findall('[\+\-]', first_add_sub)  # 提取运算符号
        # print(first_add_sub_sym)    #['-']

        if '-' in first_add_sub_sym:  # 判断运算符并进行真实运算
            result_add_sub = first_dig - second_dig
            # print(result_add_sub,print(type(result_add_sub)))
            result_add_sub_str = str(result_add_sub)  # 将结果转化为字符串
            # print(result_add_sub_str,type(result_add_sub_str))      #-5.0 <class 'str'>
        else:  # 加法进行下面的操作和上面除法操作一样
            result_add_sub = first_dig + second_dig
            # print(result_add_sub,print(type(result_add_sub)))
            result_add_sub_str = str(result_add_sub)  # 将结果转化为字符串
            # print(result_add_sub_str, type(result_add_sub_str))  # -5.0 <class 'str'>

        print(bracket_content_after_md,type(bracket_content_after_md),first_add_sub,type(first_add_sub),type(result_add_sub_str))
        #60+-3818009.3809523815 <class 'str'> 60-3818009.3809523815 <class 'str'> <class 'str'>
        #下面要进行替换操作

        bracket_content_after_md = result_add_sub_str
        print(bracket_content_after_md,result_add_sub_str)
        return add_sub(bracket_content_after_md)










    elif re.search('(\d+\.?\d*)[\+\-](\d+\.?\d*)', bracket_content_after_md):
        first_add_sub = re.search('(\d+\.?\d*)[\+\-](\d+\.?\d*)', bracket_content_after_md).group()     #提取加减法表达式
        # print(first_add_sub,type(first_add_sub))        #3-8.0 <class 'str'>
        first_add_sub_dig = re.split('\+|\-', first_add_sub)    #将数字和+ - 号分离
        # print(first_add_sub_dig)    #['3', '8.0']

        if bracket_content_after_md[0] == '-':      #加个负号判断
            first_dig = -float(first_add_sub_dig[0])    #如果第一位是负号，这将第一个数字变为负数
            bracket_content_after_md = bracket_content_after_md[1:]   #将这个负号去掉，因为已经变成负数了
            # print(bracket_content_after_md)
        else:
            first_dig = float(first_add_sub_dig[0])
        # print(first_dig)    #3.0
        second_dig = float(first_add_sub_dig[1])
        # print(second_dig)   #8.0
        first_add_sub_sym = re.findall('[\+\-]',first_add_sub)     #提取运算符号
        # print(first_add_sub_sym)    #['-']

        if '-' in first_add_sub_sym:        #判断运算符并进行真实运算
            result_add_sub = first_dig - second_dig
            # print(result_add_sub,print(type(result_add_sub)))
            result_add_sub_str = str(result_add_sub)  # 将结果转化为字符串
            # print(result_add_sub_str,type(result_add_sub_str))      #-5.0 <class 'str'>
        else:   #加法进行下面的操作和上面除法操作一样
            result_add_sub = first_dig + second_dig
            # print(result_add_sub,print(type(result_add_sub)))
            result_add_sub_str = str(result_add_sub)  # 将结果转化为字符串
            # print(result_add_sub_str, type(result_add_sub_str))  # -5.0 <class 'str'>

        bracket_content_after_as = bracket_content_after_md.replace(first_add_sub, result_add_sub_str)  #替换运算结果

        bracket_content_after_md = bracket_content_after_as

        return add_sub(bracket_content_after_md)    ##迭代处理加减

    else:
        return bracket_content_after_md  ##迭代处理加减


def mul_div(bracket_content):   #乘除法--处理括号内所有乘除法
    print("处理乘法运算: %s" %bracket_content)  #-3-40.0/5

    if re.search('(\d+\.?\d*)((\*\-)|(\/\-))(\d+\.?\d*)',bracket_content):        #提取并处理*-，/-，
        first_mul_div = re.search('(\d+\.?\d*)((\*\-)|(\/\-))(\d+\.?\d*)', bracket_content).group()
        first_mul_div_dig = re.split('((\*\-)|(\/\-))', first_mul_div)
        # print(first_mul_div)    #2*-11.0
        first_mul_div_dig = re.split('\*|\/', first_mul_div)     #提取乘法运算的两个数字
        # print(first_mul_div_dig)    #['2', '-11.0']
        first_dig = float(first_mul_div_dig[0])  # 提取第一个数字并转化格式
        # print(first_dig)    #2.0
        second_dig = float(first_mul_div_dig[1])   # 提取第二个数字并转化格式
        # print(second_dig)
        first_mul_div_sym = re.findall('[\*\/]', first_mul_div)  # 提取运算符号
        # print(first_mul_div_sym)
        if '/' in first_mul_div_sym:    #判断运算符并进行真实运算
            result_mul_dig = first_dig / second_dig
            # print(result_mul_dig,print(type(result_mul_dig)))
            result_mul_dig_str = str(result_mul_dig)    #将结果转化为字符串
            # print(result_mul_dig_str,type(result_mul_dig_str))
        else:   #乘法进行下面的操作和上面除法操作一样
            result_mul_dig = first_dig * second_dig
            # print(result_mul_dig)
            result_mul_dig_str = str(result_mul_dig)
            # print(result_mul_dig_str, type(result_mul_dig_str))

        bracket_content_after_md = bracket_content.replace(first_mul_div,result_mul_dig_str)    #替换运算结果
        # print(bracket_content_after_md)     #-3-8.0

        bracket_content = bracket_content_after_md
        # print(bracket_content)

        return mul_div(bracket_content)     #迭代处理乘除

    elif re.search('(\d+\.?\d*)[\*\/](\d+\.?\d*)',bracket_content):
        first_mul_div = re.search('(\d+\.?\d*)[\*\/](\d+\.?\d*)',bracket_content).group()   #提取第一个带有次乘除符号表达式 40.0/5，group将对象转为字符串
        # print(first_mul_div,print(type(first_mul_div)))    #40.0/5

        first_mul_div_dig = re.split('\*|\/',first_mul_div)     #提取乘法运算的两个数字
        # print(first_mul_div_dig)    #['40.0', '5']
        first_dig = float(first_mul_div_dig[0])     #提取第一个数字并转化格式
        # print(first_dig,type(first_dig))        #40.0 <class 'float'>
        second_dig = float(first_mul_div_dig[1])
        # print(second_dig, type(second_dig))     #5.0 <class 'float'>

        first_mul_div_sym = re.findall('[\*\/]',first_mul_div)      #提取运算符号
        # print(first_mul_div_sym,type(first_mul_div_sym[0]))        #['/']

        if '/' in first_mul_div_sym:    #判断运算符并进行真实运算
            result_mul_dig = first_dig / second_dig
            # print(result_mul_dig,print(type(result_mul_dig)))
            result_mul_dig_str = str(result_mul_dig)    #将结果转化为字符串
            # print(result_mul_dig_str,type(result_mul_dig_str))
        else:   #乘法进行下面的操作和上面除法操作一样
            result_mul_dig = first_dig * second_dig
            # print(result_mul_dig)
            result_mul_dig_str = str(result_mul_dig)
            # print(result_mul_dig_str, type(result_mul_dig_str))

        bracket_content_after_md = bracket_content.replace(first_mul_div,result_mul_dig_str)    #替换运算结果
        # print(bracket_content_after_md)     #-3-8.0

        bracket_content = bracket_content_after_md
        # print(bracket_content)

        return mul_div(bracket_content)     #迭代处理乘除

    else:       #返回处理乘除后结果
        return bracket_content


        # add_sub(bracket_content_after_md)   #调用加减法



def deep_bracket(expression): #处理小括号
    if re.search('\(([\-\+\*\/]*\d+\.?\d*)+\)',expression):     #有小括号则提取并处理
        bracket = re.search('\(([\-\+\*\/]*\d+\.?\d*)+\)',expression).group()   #提取第一个小括号
        # print(bracket)  #(-3-40.0/5)
        bracket_content= bracket.split("(")[1].split(")")[0]    #去除括号
        # print(bracket_content)  #-3-40.0/5
        bracket_content_after_md = mul_div(bracket_content)    #调用乘除法函数，先算乘除
        # print(bracket_content_after_md,type(bracket_content_after_md))      #9-3.3333333333333335+173134.50000000003+405.7142857142857 <class 'str'>

        print('=======================')
        bracket_content_after_as = add_sub(bracket_content_after_md)    #此为第一个小括号的计算结果
        # print(bracket_content_after_as)     #173527.88095238098

        expression = expression.replace(bracket,bracket_content_after_as)
        print("表达式为: %s" %expression)

        deep_bracket(expression)




    else:   #没有小括号交给乘法和加法处理
        mul_div(expression)

if __name__ == "__main__":
    expression = input("请输入表达式>>:")
    deep_bracket(expression)






