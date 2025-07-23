import numpy as np
import matplotlib.pyplot as plt
delta_Cvh = -4.9
delta_mvh = 3.9
delta_Tr = -9.5

t_ot = 2000
t = np.arange(0, 2000, 0.1)
ct = 4187
sig = 0.12
S = 0.75
P0 = 7900
P1 = 7600
Cvh = 22#Возможно нужно взять 17
C_vih = 22.92
Tr = 90
r = 2.26 * 10**6
kt = 5000
F = 10
Tp = 132
mvh = 12
mvt = 1.022

M = S*(((mvh - mvt)/sig)**2 + P1 - P0)
m_vih = sig * (P0 + (M / S) - P1) ** 0.5

figure, axis = plt.subplots(3, 2)
figure.tight_layout(pad=3.0)

def del_M(m_vh, T):
    return m_vh - m_vih + ((kt*F*(T - Tr))/(r - ct*Tr))

def del_C(m_vh, C_vh, C_vih, T):
    return (m_vh*C_vh - C_vih*(m_vih + del_M(m_vh, T)))/M

C_c = [C_vih]
for i, tl in enumerate(t):
    dC_dt = del_C(mvh, (Cvh+delta_Cvh), C_vih, Tp)
    C_vih = C_c[i - 1] + (0.1 * dC_dt)
    if not i == 0:
        C_c.append(C_c[i - 1] + (0.1 * dC_dt))
    # print(dC_dt)

axis[0, 0].plot(t, C_c)
axis[0, 1].plot(t, np.ones(t_ot*10)*Cvh, '--', color='r')
axis[0, 1].plot(t, np.ones(t_ot*10)*(Cvh+delta_Cvh))

C_vih = 22.92
C_m = [C_vih]
for i, tl in enumerate(t):
    dC_dt = del_C((mvh+delta_mvh), Cvh, C_vih, Tp)
    C_vih = C_m[i - 1] + (0.1 * dC_dt)
    if not i == 0:
        C_m.append(C_m[i - 1] + (0.1 * dC_dt))
print(C_m)

axis[1, 0].plot(t, C_m)
axis[1, 1].plot(t, np.ones(t_ot*10)*mvh, '--', color='r')
axis[1, 1].plot(t, np.ones(t_ot*10)*(mvh+delta_mvh))

C_vih = 22.92
C_t = [C_vih]
for i, tl in enumerate(t):
    dC_dt = del_C(mvh, Cvh, C_vih, (Tp+delta_Tr))
    C_vih = C_t[i - 1] + (0.1 * dC_dt)
    if not i == 0:
        C_t.append(C_t[i - 1] + (0.1 * dC_dt))
    # print(dC_dt)

axis[2, 0].plot(t, C_t)
axis[2, 1].plot(t, np.ones(t_ot*10)*Tp, '--', color='r')
axis[2, 1].plot(t, np.ones(t_ot*10)*(Tp+delta_Tr))
for idx, row in enumerate(axis):
    for jdx, ax in enumerate(row):
        ax.grid()
        ax.set_xlabel('$T$', fontsize=12)
        if jdx == 0:
            ax.set_ylabel('$Свых$', fontsize=12)
        else:
            if idx==1:
                ax.set_ylabel('$m_вх$', fontsize=12)
            elif idx==0:
                ax.set_ylabel('$Cвх$', fontsize=12)
            else:
                ax.set_ylabel('$Tp$', fontsize=12)

plt.show()