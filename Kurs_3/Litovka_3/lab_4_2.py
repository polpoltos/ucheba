import math
import matplotlib.pyplot as plt
import numpy as np


def function(x1, x2):
    return ((((x1 - 2)*math.cos(10)+(x2)*math.sin(10))**2)/1 + ((((x2)*math.cos(10) -  (x1 - 2)*math.sin(10))**2)/25))


def limit_1(x1, x2):
    limit = 1 - (x1/np.sin(x1) + x2/np.cos(x2))
    # limit =-1*(x1 * (x2**2)) - 1
    return limit

def limit_2(x1, x2):
    # return x1 + 1
    return x1

def function_in(x1, x2, k):
     return k* (min(0, limit_1(x1, x2))**2 + min(0, limit_2(x1, x2))**2)

def R1(x1,x2):
    k = 100
    print(function(x1,x2) + function_in(x1,x2,k))
    return function(x1,x2) + function_in(x1,x2,k)

def draw(x, y):
    x1 = np.linspace(-5, 30, 300)
    x2 = np.linspace(-5, 30, 300)
    X1, X2 = np.meshgrid(x1, x2)
    Z = function(X1, X2)
    plt.contour(X1, X2, Z, levels=30)
    limit1 = (1 - (X1 / np.sin(X1)) + (X2 / np.cos(X2)))
    limit2 = X1
    mask = (limit1 >= 0) & (limit2 >= 0)
    plt.contourf(X1, X2, mask, cmap='Greens', levels=30)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('Линии уровня функции двух переменных')
    plt.plot(x, y, 'o-', color='b')
    plt.show()

def gradient(x0, y0):
    X = []
    Y = []
    E = 0.001
    X.append(x0)
    Y.append(y0)
    delta = 0.05
    h = 1
    x_d = function(X[-1] + delta, Y[-1]) - function(X[-1], Y[-1])
    y_d = function(X[-1], Y[-1] + delta) - function(X[-1], Y[-1])
    X.append(X[-1] - h * x_d)
    Y.append(Y[-1] - h * y_d)
    while True:
        x_d = function(X[-1] + delta, Y[-1]) - function(X[-1], Y[-1])
        y_d = function(X[-1], Y[-1] + delta) - function(X[-1], Y[-1])
        X.append(X[-1] - h * x_d)
        Y.append(Y[-1] - h * y_d)
        if (R1(X[-1], Y[-1])) > 3:
            break

    print(X,Y)
    draw(X,Y)

gradient(18,0)