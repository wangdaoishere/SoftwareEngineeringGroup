from utils import *



def mySin(x):



    y = 0
    inductionFormula(x,y)     #诱导公式限制弧度制的输入为-π到π之间
    i=1                       #泰勒展开式项数标识位
    f=1                       #正负标识位
    s3=0                      #结果值
    num=0                     #
    n=10                      #泰勒展开式项数


    while True:

         g = 2*i-1            #项数的值
         b = myFactorial(g)   #阶乘结果
         t = myPower(y,g)     #乘方结果
         s3 += t * f / b      #单项结果累加
         i += 1
         num += 1
         f = -f               #正负标识位
         if(num == n):
            break

    return s3

x = 3* myPI
print(mySin(x))