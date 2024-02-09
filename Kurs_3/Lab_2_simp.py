import math
import matplotlib.pyplot as plt
import numpy as np
E = 0.01
beta = 2



def Function1(x1, x2):
    return ((((x1 - 9)*math.cos(55)+(x2 + 6)*math.sin(55))**2)/4 + (((x2+6)*math.cos(55) - (x1 - 9)*math.sin(55))**2)/9)


def Function2(x1, x2):
    return 100 * (x2 - x1 ** 2) ** 2 + (1 - x1) ** 2


def Function(x1, x2):
    return Function1(x1, x2)

def plotCreator(fx, fy):
    x = np.arange(-20, 20, 0.01)
    y = np.arange(-20, 20, 0.01)
    [X, Y] = np.meshgrid(x, y)
    plt.contour(X, Y, Function(X, Y))
    plt.plot(fx, fy,"o-")
    print(fx[-1], fy[-1])
    plt.plot(float(fx[-1]), float(fy[-1]), "x-", color='r')
    plt.show()


def main():
    print("Введите X-координату: ")
    x = float(input())
    print("Введите Y-координату: ")
    y = float(input())
    X, Y = MethodSimplex([x, y])
    plotCreator(X, Y)


def MethodSimplex(X0):
    X = []
    Y = []

    x0 = X0[0]
    y0 = X0[1]
    X.append(x0)
    Y.append(y0)
    x1 = x0 + 3
    y1 = y0
    X.append(x1)
    Y.append(y1)

    x2 = x0
    y2 = y0 + 4
    X.append(x2)
    Y.append(y2)
    X.append(x0)
    Y.append(y0)

    f0 = Function(x0, y0)
    f1 = Function(x1, y1)
    f2 = Function(x2, y2)
    i = 0
    while True:
        b = beta
        fx = max(f0, f1, f2)
        if fx == f0:
            dx = (x1 + x2) / 2 - x0
            dy = (y1 + y2) / 2 - y0

            while True:
                if Function(x0 + b * dx, y0 + b * dy) < Function(x0, y0):

                    X.append(x0)
                    Y.append(y0)

                    x0 = x0 + b * dx
                    y0 = y0 + b * dy
                    f0 = Function(x0, y0)

                    X.append(x0)
                    Y.append(y0)

                    X.append(x1)
                    Y.append(y1)

                    X.append(x2)
                    Y.append(y2)

                    X.append(x0)
                    Y.append(y0)

                    break
                else:
                    b = b * 0.96
                if b < E:
                    break
        elif fx == f1:
            dx = (x0 + x2) / 2 - x1
            dy = (y0 + y2) / 2 - y1
            while True:
                if Function(x1 + b * dx, y1 + b * dy) < Function(x1, y1):

                    X.append(x1)
                    Y.append(y1)

                    x1 = x1 + b * dx
                    y1 = y1 + b * dy
                    f1 = Function(x1, y1)

                    X.append(x1)
                    Y.append(y1)

                    X.append(x2)
                    Y.append(y2)

                    X.append(x0)
                    Y.append(y0)

                    X.append(x1)
                    Y.append(y1)

                    break
                else:
                    b = b * 0.96
                if b < E:
                    break
        else:
            dx = (x0 + x1) / 2 - x2
            dy = (y0 + y1) / 2 - y2
            while True:
                if Function(x2 + b * dx, y2 + b * dy) < Function(x2, y2):

                    X.append(x2)
                    Y.append(y2)

                    x2 = x2 + b * dx
                    y2 = y2 + b * dy
                    f2 = Function(x2, y2)

                    X.append(x2)
                    Y.append(y2)

                    X.append(x0)
                    Y.append(y0)

                    X.append(x1)
                    Y.append(y1)

                    X.append(x2)
                    Y.append(y2)

                    break
                else:
                    b = b * 0.96
                if b < E:
                    break
        if b < E:
            print("Точка 1 = ", x0, y0)
            print("Точка 2 = ", x1, y1)
            print("Точка 3 = ", x2, y2)
            break
        i = i + 1
    print("Кол-во итераций: ", i)
    return X, Y

if __name__ == "__main__":
    main()