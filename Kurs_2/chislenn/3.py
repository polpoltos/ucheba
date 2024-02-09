import sympy as sym
from sympy import *


def ucal(u, n):
    if (n == 0):
        return 1

    temp = u
    for i in range(1, int(n / 2 + 1)):
        temp = temp * (u - i)

    for i in range(1, int(n / 2)):
        temp = temp * (u + i)

    return temp



def fact(n):
    f = 1
    for i in range(2, n + 1):
        f *= i

    return f



n = 6;
x = [0.180, 0.185, 0.190, 0.195, 0.200, 0.205]


y = [[0 for i in range(n)]
     for j in range(n)]
y[0][0] = 5.61543
y[1][0] = 5.46693
y[2][0] = 5.32634
y[3][0] = 5.19304
y[4][0] = 5.06649
y[5][0] = 4.94619


for i in range(1, n):
    for j in range(n - i):
        y[j][i] = y[j + 1][i - 1] - y[j][i - 1]

def func(value):

    sum = (y[2][0] + y[3][0]) / 2

    k = 0
    if ((n % 2) > 0):
        k = int(n / 2)
    else:
        k = int(n / 2 - 1)

    u = (value - x[k]) / (x[1] - x[0])

    for i in range(1, n):

        if (i % 2):
            sum = sum + ((u - 0.5) *
                     ucal(u, i - 1) * y[k][i]) / fact(i)
        else:
            sum = sum + (ucal(u, i) * (y[k][i] + y[k - 1][i]) / (fact(i) * 2))
            k -= 1
    return sum
value = [0.1838, 0.1875, 0.1944, 0.1976, 0.2038]
for i in value:
    print("X:", i, "Y:", round(func(i),5))
x_sym = sym.Symbol('x')
polinom = func(x_sym)
print("ПОЛИНОМЧИК:")
print(simplify(polinom))
h = 0.005
derivative_f = polinom
q = (x_sym - x[0]) / h
q2 = q
factorial = 1

for j in range(1, n+1):
    q2 *= (q**2 - j**2)

for i in range(1, n):
    derivative_f = derivative_f.diff(x_sym)

for i in range(2, 2*n+3):
    factorial *= i

res_mem = ((h ** (2*n + 2)) * q2 * derivative_f * value[0]) * (q-(n+1)) / factorial
print("Остаточный член: ", '\n', res_mem)
