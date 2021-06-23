from utils import *
from mysin import *


def myCos(x, inputFlag):       #inputFlag为1，角度，inputFlag为2，弧度

    y = x + 0.5 * myPI          #sin函数与cos函数的转换

    return (mySin(y,inputFlag))


x =  0

print(myCos(x,2))