from math import pi
from math import fabs
from utils import *


def asin(x):
    result = x
    result_a = 1.0
    result_b = 1.0
    result_c = 1.0
    ii = 0
    if (x == 1 ):
        result = 90

    elif (x == -1):

        result = -90

    elif ((x < 1) and (x > -1)):
        result = x
        ii = x
        n  = 1
        while(fabs(ii) >= 1e-9):
            ii = ii * (2 * n -1) * (2 * n -1) * x * x / ((2 * n) * (2 * n +1))
            n = n + 1
            result += ii
        return round((result*180/pi))
    else:
        error = True
        return error
    
##获取结果

#print(asin(-1))
#print(asin(1))
#测试角度为90， -90 ， 30的典型值，输出可判断是否为正确的输出弧度
#print(asin(0.5))