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
def inductionFormula(x,y):

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
