import re

a = '9-2*5/3+7/3*99/4*2998+10*568/14'

b = re.search('(\d+\.?\d*)[\*\/](\d+\.?\d*)',a)

# print(b)

c = '40/5'

d = re.search('\/',c).group()
e = re.split()
print(d)


