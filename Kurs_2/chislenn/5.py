import math
import matplotlib.pyplot as plt

x_0 = -1
y_0 = 8
b = 2*math.pi - 1
h_0 = 0.5
ys, xs = [], []
y_i = y_0
dy2List = []

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

h1 = h_0
h2 = h_0 / 2
e = 0.001
r = 4

y1 = func(x_0 + h1, y_0, h1)
y2 = func(x_0 + h2, y_0, h2)
sigma = math.fabs((y1 - y2) / (math.pow(2, r) + 1))

if (sigma >= e):
    h = h2
else:
    h = h1

x_0 += h
yi = func(x_0, y_0, h)
xList = []
yList = []
dyList = []
xList.append(x_0)
yList.append(yi)
dyList.append(f(x_0, yi))



h = (b - (-1.0)) / 50
x_0 = -1.0
y_0 = 8.0

ys.append(y_0)
xs.append(x_0)
dy2List.append(f(x_0, y_0))
y_i = y_0

while x_0 < b:
    x_0 += h
    y_i = func(x_0, y_i, h)
    ys.append(y_i)
    xs.append(x_0)
    dy2List.append(f(x_0, y_i))

print("С постоянным шагом:")
for i in range(50):
    print("X[", i, "] =", xs[i], "Y[", i, "] =", ys[i])



plt.plot(xs, ys, label='Метод Рунге-Кутта третьего порядка с постоянным шагом')
# plt.plot(xs, dy2List, label='Производная')
# plt.plot(xList, yList, label='Метод Рунге-Кутта третьего порядка с автоматическим выбором шага')
# plt.plot(xList, dyList, label='С автоматическим выбором шага производная')

plt.legend()
plt.show()
