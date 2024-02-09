import math
import numpy as np
import random
a = 0
b = 2*math.pi
arr = []
arr = np.arange(a, b, 0.0000001)
mas = []
mas = np.reshape(arr, (int(len(arr)/2), 2))
N = (mas.shape[0])
print("Количество интервалов равно:", N)

def fun(a, b):
    n = 1/(5-3*math.cos(a+(b-a)*0.8))
    return n


sum = 0
for i in range(N + 1):
    sum += fun(a,b)

opr_int = ((b-a)/N)*sum
print("Определенный интеграл с количеством интервалов N, от 0 до 2*pi, функции 1/(5-3*cos(x)) равен:", opr_int)

M = 2*N
sum2 = 0
for i in range(M + 1):
    sum2 += fun(a,b)

opr_int2 = ((b-a)/M)*sum2
print("Определенный интеграл с количеством интервалов 2*N, от 0 до 2*pi функции 1/(5-3*cos(x)) равен:", opr_int2)

print("Погрешность равна:", opr_int2-opr_int)
