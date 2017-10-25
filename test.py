import re
bracket_content = '1-2*-10*(-9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))'

a = re.search('(\d+\.?\d*)((\*\-)|(\/\-))(\d+\.?\d*)',bracket_content).group()

print(a)