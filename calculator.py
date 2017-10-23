# -*- coding:utf-8 -*-
import re
import sys
import os

# expression='1-2*((60+2*(-3-40.0/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'
#
# content=re.search('\(([\-\+\*\/]*\d+\.?\d*)+\)',expression).group() #(-3-40.0/5)

def add_sub(): #加减法
    pass

def mul_div():   #乘除法
    pass

def deep_bracket(): #处理小括号
    bracket = re.search('\(([\-\+\*\/]*\d+\.?\d*)+\)',expression).group()   #提取第一个小括号
    # print(bracket)  #(-3-40.0/5)
    bracket_content= bracket.split("(")[1].split(")")[0]    #去除括号
    print(bracket_content)  #-3-40.0/5


if __name__ == "__main__":
    expression = input("请输入表达式>>:")
    deep_bracket()






