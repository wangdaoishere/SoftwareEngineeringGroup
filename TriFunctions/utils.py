from math import pi


def deg2rad(x):
    '''
    
    :param x: 输入参数为角度值
    :return x :输出为弧度数值
    
    '''
    x = x/180
    x = x*pi
    return x

def rad2deg(x):
    '''
    
     :param x: 输入参数为弧度数值
     :return x :输出为角度值
     
    '''
    x = x/pi
    x = x*180
    return x

