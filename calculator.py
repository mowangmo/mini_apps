# -*- coding:utf-8 -*-
import re
import sys
import os
import json

# expression='1-2*((60+2*(-3-40.0/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
# expression='1-2*10*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
# content=re.search('\(([\-\+\*\/]*\d+\.?\d*)+\)',expression).group() #(-3-40.0/5)

def add_sub(bracket_content_after_md): #加减法
    print(bracket_content_after_md)     #3-8.0
    if re.search('(\d+\.?\d*)[\+\-](\d+\.?\d*)', bracket_content_after_md):
        first_add_sub = re.search('(\d+\.?\d*)[\+\-](\d+\.?\d*)', bracket_content_after_md).group()
        print(first_add_sub,type(first_add_sub))        #3-8.0 <class 'str'>
        first_add_sub = re.split('\+|\-', first_add_sub)    #将数字和+ - 号分离
        print(first_add_sub)    #['3', '8.0']
        first_dig = float(first_add_sub[0])
        # print(first_dig)    #3.0
        second_dig = float(first_add_sub[1])
        # print(second_dig)   #8.0
        first_add_sub_sym = re.findall('[\+\-]',first_add_sub)     #提取运算符号
        print(first_add_sub_sym)

def mul_div(bracket_content):   #乘除法--处理括号内所有乘除法
    # print(bracket_content)  #-3-40.0/5
    if re.search('(\d+\.?\d*)[\*\/](\d+\.?\d*)',bracket_content):
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



def deep_bracket(): #处理小括号
    if re.search('\(([\-\+\*\/]*\d+\.?\d*)+\)',expression):     #有小括号则提取并处理
        bracket = re.search('\(([\-\+\*\/]*\d+\.?\d*)+\)',expression).group()   #提取第一个小括号
        # print(bracket)  #(-3-40.0/5)
        bracket_content= bracket.split("(")[1].split(")")[0]    #去除括号
        # print(bracket_content)  #-3-40.0/5
        bracket_content_after_md = mul_div(bracket_content)    #调用乘除法函数，先算乘除
        # print(bracket_content_after_md,type(bracket_content_after_md))      #9-3.3333333333333335+173134.50000000003+405.7142857142857 <class 'str'>
        add_sub(bracket_content_after_md)

    else:   #没有小括号交给乘法和加法处理
        mul_div(expression)

if __name__ == "__main__":
    expression = input("请输入表达式>>:")
    deep_bracket()






