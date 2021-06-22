#本文件提供 阶乘函数 与 幂函数
#阶乘函数
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