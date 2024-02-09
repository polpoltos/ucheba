import math
import matplotlib.pyplot as plt
import numpy as np

x_0 = -1
y_0 = 8
b = 2*math.pi - 1
h_0 = 0.5
ys, xs = [], []
y_i = y_0
dy2List = []
arr = []
arr = np.arange(x_0, b, 0.00005)
mas = []
mas = np.reshape(arr, (int(len(arr)/2), 2))
N = (mas.shape[0])


def func(x_0, y_0, h):
    k1 = h * f(x_0, y_0)
    k2 = h * f(x_0 + h/3, y_0 + k1/3)
    k3 = h * f(x_0 + (2*h)/3, y_0 + (2*k2)/3)
    return y_0 + (k1/4 + (3*k3)/4)

def f(x, y):
    return F(x) - g(x) * y

def F(x):
    return phi(x)*0.001

def phi(x):
    return math.exp(-1 * pow(x, 2))

def g(x):
    return -1*(math.sin(x+1))

h = (b - (-1.0)) / N
x_0 = -1.0
y_0 = 8.0
ys.append(y_0)
xs.append(x_0)
dy2List.append(f(x_0, y_0))
y_i = y_0

for i in range(N):
    x_0 += h
    y_i = func(x_0, y_i, h)
    ys.append(y_i)
    xs.append(x_0)
    dy2List.append(f(x_0, y_i))


plt.plot(xs, ys, label='Рунге-Кутта 3-ого порядка с постоянным шагом')



plt.legend()
plt.show()
