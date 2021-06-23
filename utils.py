#本文件提供 阶乘函数 与 幂函数
#阶乘函数
myPI = 3.1415926535897932

def myFactorial(a):
    sum=1
    for i in range(1,a+1):
         sum*=i
    return sum

#幂函数

def myPower(x,t):
    m=1
    i=1
    while i<=t:
       m *= x
       i += 1
    return m

#诱导公式使定义域收敛
def inductionFormula(x):


    if x > myPI:

        while True:

            x -= (2 * myPI)

            if x <= myPI:
                y = x
                break
    elif x < (-1 * myPI):

        while True:

            x += (2 * myPI)

            if x >= (-1 * myPI):
                y = x
                break
    else: y = x

    return y

#绝对值函数

def myAbs(x):

    if x >= 0:
        x = x
    else:
        x = -x
    return x

#截尾函数，当结果应为+-0.5时，消除误差

def myRound(result):
    if(myAbs(result-0.5)<0.00000001):
        result = 0.5
    elif(myAbs(result+0.5)<0.00000001):
        result = -0.5
    elif (myAbs(result - 0) < 0.00000001):
        result = 0
    return result


