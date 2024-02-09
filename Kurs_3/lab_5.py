from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import math as mth

A = -1
B = 2
C = 2
D = 9
ALPHA = 80
E = 0.01

KEY = 0.25


def FunctionTRUE(x):
    return ((x[0] - A) * mth.cos(ALPHA) + (x[1] - B) * mth.sin(ALPHA)) ** 2 / C ** 2 + (
                (x[1] - B) * mth.cos(ALPHA) - (x[0] - A) * mth.sin(ALPHA)) ** 2 / D ** 2


def GradientFunction(x):
    return np.array(
        [-C * (-(x[0] - A) * mth.sin(ALPHA) + (x[1] - B) * mth.cos(ALPHA)) * mth.sin(ALPHA) / D ** 2 + 2 * (
                    (x[0] - A) * mth.cos(ALPHA) + (x[1] - B) * mth.sin(ALPHA)) * mth.cos(ALPHA) / C,
         C * (-(x[0] - A) * mth.sin(ALPHA) + (x[1] - B) * mth.cos(ALPHA)) * mth.cos(ALPHA) / D ** 2 + 2 * (
                     (x[0] - A) * mth.cos(ALPHA) + (x[1] - B) * mth.sin(ALPHA)) * mth.sin(ALPHA) / C])


def FineFirst(X):
    return 3 * X[1]**3 - X[0]**2 - 2


def FineEqual(X):
    return X[0] + X[1] + 1


def FunctionFine(X, K):
    if FineFirst(X) > 0:
        return K * mth.log(FineFirst(X))
    else:
        return 0


def FunctionEquality(X, K):
    return K * FineEqual(X) ** 2


def Function(X, K):
    a = FunctionTRUE(X)
    b = FunctionEquality(X, K)
    c = FunctionFine(X, K)
    return a + b + c


def MethodSimplex(x0, K):
    x1 = x0
    x2 = np.array([x0[0] + KEY, x0[1]])
    x3 = np.array([x0[0], x0[1] + KEY])
    f1 = Function(x1, K)
    f2 = Function(x2, K)
    f3 = Function(x3, K)
    last = x0
    i=0
    while True:
        alpha = 2
        fMax = max(f1, f2, f3)
        if fMax == f1:
            dx = (x2[0] + x3[0]) / 2 - x1[0]
            dy = (x2[1] + x3[1]) / 2 - x1[1]
            while True:
                x = np.array([x1[0]+alpha*dx, x1[1]+alpha*dy])
                fdX = Function(x, K)
                if fdX < f1:
                    x1 = x
                    f1 = fdX

                    last = x1
                    break
                else:
                    alpha = alpha*0.92
                if alpha < E:
                    break
        elif fMax == f2:
            dx = (x1[0] + x3[0]) / 2 - x2[0]
            dy = (x1[1] + x3[1]) / 2 - x2[1]
            while True:
                x = np.array([x2[0]+alpha*dx, x2[1]+alpha*dy])
                fdX = Function(x, K)
                if fdX < f2:
                    x2 = x
                    f2 = fdX

                    last = x2
                    break
                else:
                    alpha = alpha*0.92
                if alpha < E:
                    break
        else:
            dx = (x2[0] + x1[0]) / 2 - x3[0]
            dy = (x2[1] + x1[1]) / 2 - x3[1]
            while True:
                x = np.array([x3[0]+alpha*dx, x3[1]+alpha*dy])
                fdX = Function(x, K)
                if fdX < f3:
                    x3 = x
                    f3 = fdX
                    last = x3
                    break
                else:
                    alpha = alpha*0.92
                if alpha < E:
                    break
        i=i+1
        if alpha < E:
            break
    print("Количество итераций симплекса:", i)
    return last


def MethodFineFunction(x0):
    print('Начальная точка:')
    print(x0, '\n')
    K = 10
    iMax = 50
    X = np.zeros((2, iMax))
    x1 = x0
    X[:, 0] = x1
    xNext = 0
    if checkPoint(x1):
        print()
    else:
        print("Точка не удовлетворяет нас!")
        return None
    i = 1
    while True:
        print("Итерация: ", i)
        xNext = MethodSimplex(x1, K)
        if distance(x1, xNext) < E or i+1 > iMax:
            break
        X[:, i] = xNext
        x1 = xNext
        K = K * 10
        i = i + 1
    X = X[:, 0: i]
    print()
    print("Количество итераций для Метода штрафных функций: ", i)
    print("Точка минимума:", xNext)
    return [X]


def plotCreator(fx, fy):
    x1 = np.linspace(-30, 30, 300)
    x2 = np.linspace(-30, 30, 300)
    X1, X2 = np.meshgrid(x1, x2)
    Z = FunctionTRUE([X1, X2])
    plt.contour(X1, X2, Z, levels=30)
    limit1 = -3 * X2 ** 3 + X1 ** 2 + 2
    Z_1 = FineEqual([X1, X2])
    mask = (limit1 >= 0)
    plt.contourf(X1, X2, mask, cmap='Greens', levels=30)
    plt.contour(X1, X2, Z_1, levels=[0], cmap='plasma')
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('Линии уровня функции двух переменных')
    plt.plot(fx, fy, 'o-', color='b')
    plt.show()


def distance(X0, X1):
    return np.sqrt((X1[0] - X0[0]) ** 2 + (X1[1] - X0[1]) ** 2)


def checkPoint(X):
    if FineFirst(X) <= 0:
        return True
    else:
        return False


if __name__ == "__main__":
    x = 5
    y = -6
    list_out = MethodFineFunction([x, y])
    if list_out == None:
        plotCreator(1, 1)
    else:
        X = list_out[0]
        plotCreator(X[0, :], X[1, :])