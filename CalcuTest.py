import pytest
from function import *
def test():                 # 测试arcsin函数
    assert mySin(0)     ==  0
    assert mySin(30)    ==  0.5
    assert mySin(90)    ==  1
    assert mySin(100)  -0.98481 <=  0.0001

    assert myCos(0)     ==  1
    assert myCos(60)    ==  0.5
    assert myCos(90)    ==  0
    assert myCos(100) + 0.17364  <=  0.0001

    assert asin(-1)   ==  -90
    assert asin(0)    ==    0
    assert asin(0.5)   ==  30
    assert asin(0.6)  - 36.86989 <=    0.001

    assert atan(0)   ==  0
    assert atan(1)   ==  45
    assert atan(2) - 63.43494  <=  0.1
    assert atan(5) - 78.69006  <=  0.3

    return True




