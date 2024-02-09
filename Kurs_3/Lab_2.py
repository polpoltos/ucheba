import math
import matplotlib.pyplot as plt
import numpy as np


# Определяем функцию двух переменных
def function(x1, x2):
    # a = 3
    # b = 7
    # c = 4
    # d = 7
    # alph = 50
    return ((((x1 - 9)*math.cos(55)+(x2 + 6)*math.sin(55))**2)/4 + (((x2+6)*math.cos(55) - (x1 - 9)*math.sin(55))**2)/9)
    # return 100 * (x2 - x1**2)**2+(1-x1)**2
    # return (((x1 - a) * math.cos(alph) + (x2 - b) * math.sin(alph))**2) / (c**2) + (((x2 - b) * math.cos(alph) - (x1 - a) * math.sin(alph))**2) / (d**2)
    # return ((((x1 - 7) * math.cos(75) + (x2 + 3) * math.sin(75)) **2) / (1 **2)) + ((((x2 + 3) * math.cos(75) - (x1 - 7) * math.sin(75))**2) / (3**2))
def draw(x, y, x11, y11):
    x1 = np.linspace(-30, 30, 300)
    x2 = np.linspace(-30, 30, 300)
    X1, X2 = np.meshgrid(x1, x2)
    Z = function(X1, X2)
    plt.contour(X1, X2, Z, levels=30)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.title('Линии уровня функции двух переменных')
    plt.plot(x, y, 'x-r')
    plt.plot(x11, y11, 'o-r')
    plt.show()

def Powell(x1, x2):
    delta = 0.3
    f = function(x1, x2)
    print(f)
    flag = 1
    sp_x1 = []
    sp_x2 = []
    sp_diag_x1 = [x1]
    sp_diag_x2 = [x2]
    while True:
        if flag:
            if f > function(x1 + delta, x2):
                f = function(x1 + delta, x2)
                x1 += delta
                print(f, 1)
            elif f > function(x1 - delta, x2):
                f = function(x1 - delta, x2)
                x1 -= delta
                print(f, 2)
            else:
                flag = 0
        if flag != 1:
            if f > function(x1, x2 + delta):
                f = function(x1, x2 + delta)
                x2 += delta
                print(f, 3)
            elif f > function(x1, x2 - delta):
                f = function(x1, x2 - delta)
                x2 -= delta
                print(f, 4)
            else:
                sp_diag_x1.append(x1)
                sp_diag_x2.append(x2)
                del_x1 = sp_diag_x1[-1] - sp_diag_x1[-2]
                del_x2 = sp_diag_x2[-1] - sp_diag_x2[-2]
                while function(sp_diag_x1[-1], sp_diag_x2[-1]) < function(sp_diag_x1[-2], sp_diag_x2[-2]):
                    sp_diag_x1.append(sp_diag_x1[-1] + del_x1)
                    sp_diag_x2.append(sp_diag_x2[-1] + del_x2)
                    if function(sp_diag_x1[-1], sp_diag_x2[-1]) > function(sp_diag_x1[-2], sp_diag_x2[-2]):
                        sp_diag_x1.append(sp_diag_x1[-1] - del_x1)
                        sp_diag_x2.append(sp_diag_x2[-1] - del_x2)
                        break
                flag = 1

        if function(sp_diag_x1[-1], sp_diag_x2[-1]) < function(x1, x2):
            sp_x1.append(sp_diag_x1[-1])
            sp_x2.append((sp_diag_x2[-1]))
        else:
            sp_x1.append(x1)
            sp_x2.append(x2)
        gradient = np.array(function(sp_x1[-1], sp_x2[-1])).flatten()
        if np.linalg.norm(gradient) < 0.01:
            break

    print(f"f(x1, x2) = {function(sp_x1[-1], sp_x2[-1])} x1 = {sp_x1[-1]} x2 = {sp_x2[-1]}")
    draw(sp_x1, sp_x2, sp_diag_x1, sp_diag_x2)


Powell(20, 8)