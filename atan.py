from numpy import double

from utils import *
from utils2 import *




def atan(x, inputflag,):

        # x{-1,1}的计算
        if ((x > -1) and (x < 1)):
            # 声明变量总和，和每阶展开式数值
            sum = x, x_pow = x, item = 0.00
            # 定义正负与阶数
            n = 1 ; fact = 1 ; sign = 1

            while ((absxxxx(item)>0.000001) or (item == 0.00)):
                fact = fact * (n+1) * (n+2)
                x_pow *= x*x
                sign = -sign
                item = x_pow/ (n+2) *sign
                sum += item
                n += 2
            return sum

        #x为(1,)
        elif (x >= 1):
            sum = x + myPI/2
            x_pow = x, item = 0.00
            n = 1 ; sign = 1
            while ((absxxxx(item) > 0.000001) or (item == 0.00)):
                x_pow *= x*x
                sign = -sign
                item = -1 / (x_pow) * (n+2) *sign
                sum += item
                n +=2
            return sum



        #x为负
        elif (x <= -1):
            sum = x - myPI/2
            x_pow = x. item = 0.00
            n = 1
            sign = 1
            while ((absxxxx(item) > 0.000001) or (item == 0.00)):
                x_pow *= x * x
                sign = -sign
                item = -1 / (x_pow) * (n+2) *sign
                sum += item
                n += 2
            return sum
#将X与-pi/2,pi/2相加返回的结果值精度在0.000001







