import math
import numpy as np
import matplotlib.pyplot as plt


Kt = 6500
Ct = 4190
Ro = 1000
T = 80
L = 1
D = 0.05
U = 0.2
TauMax = 10
del_a = 0.3
del_b = 0.2
abs_Tau = L/U # Среднее время пребывания


def T_del(t0):
    return float(t0 + (T - t0) * ((4*Kt/(Ct*Ro*D))))

def plotCreator():
    T1 = []
    Tau = []
    l = []

#I
    for i in np.arange(-abs_Tau/2,0,del_b):
        T0 = 50 #T0
        for j in np.arange(-i,i+abs_Tau,del_a):
            l.append(U*(j-i))
            Tau.append(j+i)
            T0 = T_del(T0)
            T1.append(T0)
#II
    for i in np.arange(0,(TauMax-abs_Tau)/2,del_b):
        T0 = 50 #T_vh
        for j in np.arange(i,i+abs_Tau,del_a):
            l.append(U*(j-i))
            Tau.append(j+i)
            T0 = T_del(T0)
            T1.append(T0)
#III
    for i in np.arange((TauMax-abs_Tau)/2,TauMax/2,del_b):
        T0 = 50 #T_vh
        for j in np.arange(i,-i+TauMax,del_a):
            l.append(U*(j-i))
            Tau.append(j+i)
            T0 = T_del(T0)
            T1.append(T0)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(l, Tau, T1, c='r', marker='x')

    ax.set_xlabel('l')
    ax.set_ylabel('Tau')
    ax.set_zlabel('T1')

    plt.show()


if __name__ == '__main__':
    plotCreator()
