import math
def factorial(a):    # 阶乘
  b=1
  while a!=1:
    b*=a
    a-=1
  return b
def taylor(x,n):
  a=1
  x = x/180*(math.pi)    # 转换为弧度
  count=1
  for k in range(1,n):
    if count%2!=0:
      a-=(x**(2*k))/factorial(2*k)
    else:
      a+=(x**(2*k))/factorial(2*k)
    count+=1
  return a
def cos(x):
  return round(taylor(x,50),3)

# print(cos(5))

