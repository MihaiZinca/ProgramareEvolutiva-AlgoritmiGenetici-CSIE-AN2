import numpy as np

def mod(a):
    b=a
    b[0][0]=23
    return b

a=[[0,0,0],[1,1,1]]
b=mod(a)
print(a)
print(b)