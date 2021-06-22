from utils import *



def mySin(x):
    i=1                       #泰勒展开式项数标识位
    f=1                       #正负标识位
    s3=0                      #结果值
    num=0                     #
    n=10                      #泰勒展开式项数


    while True:

         g = 2*i-1            #项数的值
         b = myFactorial(g)   #阶乘结果
         t = myPower(x,g)     #乘方结果
         s3 += t * f / b      #单项结果累加
         i += 1
         num += 1
         f = -f               #正负标识位
         if(num == n):
            break

    return s3

