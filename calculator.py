# -*- coding:utf-8 -*-
import re
import sys
import os
import json

# expression='1-2*((60+2*(-3-40.0/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
# expression='1-2*10*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
# content=re.search('\(([\-\+\*\/]*\d+\.?\d*)+\)',expression).group() #(-3-40.0/5)

def add_sub(): #加减法
    pass

def mul_div(bracket_content):   #乘除法
    # first_mul_div = re.search(,bracket_content)
    # print(bracket_content)  #-3-40.0/5
    first_mul_div = re.search('(\d+\.?\d*)[\*\/](\d+\.?\d*)',bracket_content).group()   #提取第一个带有次乘除符号表达式 40.0/5，group将对象转为字符串
    print(first_mul_div)    #40.0/5
    first_mul_div_dirc = re.split('\*|\/',first_mul_div)
    print(first_mul_div_dirc)

    # mul = re.findall('\/',first_mul_div)    #提取除号，如果没有除号则有乘号
    # print(mul)  #['/']
    # if len(mul):
    #     first_mul_div.split()






def deep_bracket(): #处理小括号
    bracket = re.search('\(([\-\+\*\/]*\d+\.?\d*)+\)',expression).group()   #提取第一个小括号
    # print(bracket)  #(-3-40.0/5)
    bracket_content= bracket.split("(")[1].split(")")[0]    #去除括号
    # print(bracket_content)  #-3-40.0/5
    mul_div(bracket_content)    #调用乘除法函数，先算乘除


if __name__ == "__main__":
    expression = input("请输入表达式>>:")
    deep_bracket()






