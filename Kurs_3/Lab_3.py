import math
import matplotlib.pyplot as plt
import numpy as np


# Определяем функцию двух переменных
def function(x1, x2):
    # return ((((x1 - 9)*math.cos(55)+(x2 + 6)*math.sin(55))**2)/4 + ((((x2+6)*math.cos(55) -  (x1 - 9)*math.sin(55))**2)/9))
    # return 100 * (x2 - x1**2)**2+(1-x1)**2
    return ((((x1 - 7) * math.cos(75) + (x2 + 3) * math.sin(75)) **2) / (1 **2)) + ((((x2 + 3) * math.cos(75) - (x1 - 7) * math.sin(75))**2) / (3**2))


def draw(x, y):
    x1 = np.linspace(-30, 30, 300)
    x2 = np.linspace(-30, 30, 300)
    X1, X2 = np.meshgrid(x1, x2)
    Z = function(X1, X2)
    plt.contour(X1, X2, Z, levels=30)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('Линии уровня функции двух переменных')
    plt.plot(x, y, 'o-', color='b')
    plt.plot(x[-1], y[-1], 'x-', color = 'r')
    plt.show()

def gradient(x0, y0):
    X = []
    Y = []
    E = 0.001
    X.append(x0)
    Y.append(y0)
    delta = 0.1
    h = 1
    while True:
        x_d = function(X[-1] + delta, Y[-1]) - function(X[-1], Y[-1])
        y_d = function(X[-1], Y[-1] + delta) - function(X[-1], Y[-1])
        X.append(X[-1] - h * x_d)
        Y.append(Y[-1] - h * y_d)
        if (abs(x_d) + abs(y_d)) < E:
            break
    print(X,Y)
    draw(X,Y)

gradient(20, 20)

# def rapid_descent(x0, y0):
#     X = []
#     Y = []
#     E = 0.001
#     X.append(x0)
#     Y.append(y0)
#     delta = 0.1
#     h = 1
#     x_d = function(X[-1] + delta, Y[-1]) - function(X[-1], Y[-1])
#     y_d = function(X[-1], Y[-1] + delta) - function(X[-1], Y[-1])
#     while True:
#         if function(X[-1] - h * x_d, Y[-1] - h * y_d) > function(X[-1], Y[-1]):
#             x_d = function(X[-1] + delta, Y[-1]) - function(X[-1], Y[-1])
#             y_d = function(X[-1], Y[-1] + delta) - function(X[-1], Y[-1])
#             X.append(X[-1] - h * x_d)
#             Y.append(Y[-1] - h * y_d)
#         else:
#             X.append(X[-1] - h * x_d)
#             Y.append(Y[-1] - h * y_d)
#         if (abs(x_d) + abs(y_d)) < E:
#             break
#     print(X, Y)
#     draw(X, Y)

# rapid_descent(20, 20)

