from utils import *
from math import pi
from math import pow
from math import radians
# sin函数
def mySin(x):					#inputFlag为1，角度，inputFlag为2，弧度
    # if(inputFlag==1):         #输入为角度时，将角度转换为弧度
    #     x = x * myPI / 180
    # else:
    #     x = x
	x=radians(x)
	y= inductionFormula(x)  #诱导公式限制弧度制的输入为-π到π之间
	i=1                       #泰勒展开式项数标识位
	f=1                       #正负标识位
	result=0                      #结果值
	num=0                     #
	n=10                      #泰勒展开式项数

	while True:
         g = 2*i-1            #项数的值
         b = myFactorial(g)   #阶乘结果
         t = myPower(y,g)     #乘方结果
         result += t * f / b      #单项结果累加
         i += 1
         num += 1
         f = -f               #正负标识位
         if(num == n):
            break
	result = myRound(result)   #自定义截尾函数，消除误差
	return round(result,5)

def myCos(x):       	#inputFlag为1，角度，inputFlag为2，弧度
    y = x + 90         #sin函数与cos函数的转换
    return (mySin(y))


def asin(x):
    result = x
    result_a = 1.0
    result_b = 1.0
    result_c = 1.0
    ii = 0
    if (x == 1 ):
        result = 90
        return result
    elif (x == -1):

        result = -90
        return result
    elif ((x < 1) and (x > -1)):
        result = x
        ii = x
        n  = 1
        while(myAbs(ii) >= 1e-9):
            ii = ii * (2 * n -1) * (2 * n -1) * x * x / ((2 * n) * (2 * n +1))
            n = n + 1
            result += ii
        return round((result*180/pi),5)
    else:
        error = True
        return error

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

        sum = (pi / 4) * x + 0.285 * x * (1 - myAbs(x))

    return round(sum*180/pi,5)



