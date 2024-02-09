import numpy as np
from numpy import array

A = array([[0.38, -0.05, 0.01, 0.02, 0.07],
           [0.052, 0.595, 0, -0.04, 0.04],
           [0.03, 0, 0.478, -0.14, 0.08],
           [-0.06, 1.26, 0, 0.47, -0.02],
           [0.25, 0, 0.09, 0.01, 0.56]])

b = array([[0.75],
           [-0.858],
           [3.16],
           [-1.802],
           [2.91]])
m = len(A)
x = [0.0 for i in range(m)]
Iteration = 0
converge = False
pogr = 0.
while not converge:
    x_new = np.copy(x)
    for i in range(m):
        s1 = sum(A[i][j] * x_new[j] for j in range(i))
        s2 = sum(A[i][j] * x[j] for j in range(i + 1, m))
        x_new[i] = (b[i] - s1 - s2) / A[i][i]
    pogr = sum(abs(x_new[i] - x[i]) for i in range(m))
    converge = pogr < 1e-6
    Iteration += 1
    x = x_new
print('Решение системы уравнений :', x)
