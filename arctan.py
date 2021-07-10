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
        sum = pi/4
    elif(x== -1):
        sum = -pi/4
    elif(x>1) :
        x = 1/x
        sum = (pi/4) * x +  x * (0.186982 - 0.191942 * pow(x,2))

        sum = pi/2- sum

           # sum = -(pi/2 -sum)

    elif ((x > -1) or (x < 1)):

        sum = (pi / 4) * x + 0.285 * x * (1 - absxxxx(x))

    return (sum*180/pi)

#print(atan(0))
#print(round(atan(6)*180/pi, 2))
#print(atan(6))
#print(atan(6000000))测试典型值其中2000000应该接近pi/2的值可以利用弧度转换看出接近（90°）
