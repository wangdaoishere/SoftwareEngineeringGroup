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
        for i in range(0, 15, 1):
            for ii in range(0,2*i+1, 1 ):
                result_a *= (2 * ii + 1) / (2 * ii +2)
                result_b *= x * x
            result_b *= x
            result_c = result_a / (ii + 2)
            result += result_c * result_b
            result_a = 1.0; result_b = 1.0
        return result
    else:
        error = True
        return error
    
##获取结果

#print(asin(-1))
#print(asin(1))
#print(asin(0.5))测试角度为90， -90 ， 30的典型值，输出可判断是否为正确的输出弧度
