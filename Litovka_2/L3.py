import math
import numpy as np
import matplotlib.pyplot as plot

R = 8.31
E1 = 251000
E2 = 297000
A1 = 2*10**11
A2 = 8*10**12
p = 1.4
D = 0.1
m = 3.3
Cvh = 26
L = 150
T0 = 1240
T1 = 1350
mu = 0.02805

L = 150
del_l = 0.5
L_Array = np.arange(0,L+del_l,del_l)


def C_Ne_procent(C):
    return (C*p)/(100*mu)

def K(a, e, t):
    return a*np.exp(((-e) / (R * t)))

def del_C1(C1, T):
    return (-K(A1, E1, T) * C1 * (p * (np.pi * (D ** 2)) / 4)) / m

def del_C2(C1, C2, T):
    return ((K(A1, E1, T) * C1 - K(A2, E2, T) * C2) * p * (np.pi * D ** 2) / 4) / m

fig, axes = plot.subplots(nrows=2, ncols=2, figsize=(18, 12))
axes[0][0].set_xlabel("L, метры")
axes[0][0].set_ylabel("C1, моль/м^3")
axes[0][1].set_xlabel("L, метры")
axes[0][1].set_ylabel("C2, моль/м^3")
# axes[1][0].set_xlabel("L, метры")
# axes[1][0].set_ylabel("C1, %")
# axes[1][1].set_xlabel("L, метры")
# axes[1][1].set_ylabel("С2, %")
for i in range(T0, T1, 10):
    C1 = C_Ne_procent(Cvh)
    C2 = 0
    C1_pr = C1 * 100 * 0.02805 / p
    C2_pr = C2 * 100 * 0.026038 / p
    C1_ar = []
    C2_ar = []
    C1_ar_pr = []
    C2_ar_pr = []
    for _ in L_Array:
        C1_ar.append(C1)
        C2_ar.append(C2)
        C1_ar_pr.append(C1_pr)
        C2_ar_pr.append(C2_pr)
        C1 = C1 + del_C1(C1, i) * del_l
        C2 = C2 + del_C2(C1, C2, i) * del_l
        print(C2)
        C1_pr = C1 * 100 * 0.02805 / p
        C2_pr = C2 * 100 * 0.026038 / p
    print(C2)
    axes[0][0].plot(L_Array, C1_ar)
    axes[0][1].plot(L_Array, C2_ar)
    # axes[1][0].plot(L_Array, C1_ar_pr)
    # axes[1][1].plot(L_Array, C2_ar_pr)
plot.subplots_adjust(wspace=0.5, hspace=0.5)
plot.show()

