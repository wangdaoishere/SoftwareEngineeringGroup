from utils import *
import math
# sin函数
def mySin(x):					#inputFlag为1，角度，inputFlag为2，弧度
    # if(inputFlag==1):         #输入为角度时，将角度转换为弧度
    #     x = x * myPI / 180
    # else:
    #     x = x
	x=math.radians(x)
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
	if x>=-1 and x<=1:
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
		    for i in range(0, 50, 1):
		        for ii in range(0,2*i+1, 1 ):
		            result_a *= (2 * ii + 1) / (2 * ii +2)
		            result_b *= x * x
		        result_b *= x
		        result_c = result_a / (ii + 2)
		        result += result_c * result_b
		        result_a = 1.0; result_b = 1.0
		    result=math.degrees(result)
		return round(result,5)
	else:
		error = True  #实现异常处理，当输入超出定义域范围，返回异常error
		return error

def atan(x):
    mult = 0
    sum = 0
    xx = 0
    sign = 1
    if (x == 1):
        sum = myPI / 4
    elif (x == 0):
        sum = 0
    elif (x == -1):
        sum = -myPI / 4
    elif ((x > 1) or (x < -1)):
        mult = 1 / x
        sign = -sign
        xx = mult * mult
        for i in range(1, 300, 2):
            sum += mult * sign / i
            mult *= xx
        if (x > 1):
            sum = sum + myPI / 2
        elif (x < -1):
            sum = -(myPI / 2 - sum)
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
        while ((absxxxx(item) > 0.000001) or (item == 0.00)):
            fact = fact * (n + 1) * (n + 2)
            x_pow *= x * x
            sign = -sign
            item = x_pow / (n + 2) * sign
            sum += item
            n += 2
    return round(math.degrees(sum),5)



