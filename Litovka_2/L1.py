import matplotlib.pyplot as plt
import numpy as np

Tr = 90
r = 2.26 * 10**6
kt = 5000
F = 10
ct = 4187
C0 = 17
C1 = 26
Cvh = 22
m0 = 10
m1 = 15
mvh = 12
T0 = 125
T1 = 146
Tp = 132
m = 12
mvt = (mvh*ct*Tp + kt*F*(Tp-Tr)-m*ct*Tp)/r
print(mvt)
def func(m, c, Tp):
    return (m*c)/(m - (kt*F*(Tp-Tr)/(r-ct*Tr)))

c = np.arange(C0, C1, 0.4)
y1 = func(mvh, c, Tp)
m = np.arange(m0, m1, 0.2)
y2 = func(m, Cvh, Tp)
t = np.arange(T0, T1, 0.5)
y3 = func(mvh, Cvh, t)
# print(list(c))
# print(list(y1))
for i in (list(c)):
    if i > 22 and i < 23:
       print(round(i, 2), round(func(mvh, round(i, 2), Tp), 2))
fig = plt.figure()
ax1 = fig.add_subplot(311)
ax1.plot(c, y1, 'b')
ax1.set_title('Зависимость от C')

ax2 = fig.add_subplot(312)
ax2.plot(m, y2, 'b')
ax2.set_title('Зависимость от m')

ax3 = fig.add_subplot(313)
ax3.plot(t, y3, 'b')
ax3.set_title('Зависимость от T')

plt.tight_layout()

plt.show()