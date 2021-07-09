import sys
from utils import *
from math import pi
from math import fabs
myPI = 3.1415926535897932


def absxxxx(x):
    if x >= 0 :
        return x
    else :
        return -x

def atan(x):
    mult = 0
    sum = 0
    xx = 0
    sign = 1
    if(x == 1):
        sum = myPI/4
    elif(x== -1):
        sum = -myPI/4
    elif((x>1)or(x<-1)):
        mult = 1/x
        sign = -sign
        xx = mult * mult
        for i in range(1, 300, 2):
            sum += mult * sign / i
            mult *=xx
        if(x > 1): 
            sum = sum+myPI/2
        elif(x<-1):
            sum = -(myPI/2 -sum)
        else:
            sum = sum
    elif ((x > -1) or (x < 1)):
        sum = x
        x_pow = x
        item = 1
        # 定义正负与阶数
        n = 1
        fact = 1
        sign = 1
        while ((absxxxx(item)>0.000001) or (item == 0.00)):
            fact = fact * (n+1) * (n+2)
            x_pow *= x*x
            sign = -sign
            item = x_pow/ (n+2) *sign
            sum += item
            n += 2
    return sum

#print(atan(1))
#print(atan(0)
#print(atan(6000000))测试典型值其中2000000应该接近pi/2的值可以利用弧度转换看出接近（90°）
