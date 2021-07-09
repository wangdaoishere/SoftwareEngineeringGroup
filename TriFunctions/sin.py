from math import fabs
from math import pi


def sin(x):

    x = x / 180 * pi    # 输入角度转换为弧度
    g = 0
    t = x
    n = 1

#使用泰勒展开式对sin值进行计算
    while (fabs(t) >= 1e-15):   #设置计算的精度
        g += t
        n += 1
        t = -t * x * x / (2 * n - 1) / (2 * n - 2)
    return round(g, 3)  #计算结果保留三位小数

#test
ans = sin(60)
print(ans)


