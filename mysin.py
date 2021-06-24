from utils import *



def mySin(x, inputFlag):       #inputFlag为1，角度，inputFlag为2，弧度

    if(inputFlag==1):         #输入为角度时，将角度转换为弧度
        x = x * myPI / 180
    else:
        x = x




    y =  inductionFormula(x)  #诱导公式限制弧度制的输入为-π到π之间
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

    return result

