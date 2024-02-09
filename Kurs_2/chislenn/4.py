import numpy as np

def f(x):
    return (x+1)*((x**2 + 1))**0.5


def trapezoidal(x0, xn, n):
    h = (xn - x0) / n

    integration = f(x0) + f(xn)

    for i in range(1, n):
        k = x0 + i * h
        integration = integration + 2 * f(k)

    integration = integration * h / 2

    return integration

a = 0
b = 3/4
arr = []
arr = np.arange(a, b, 0.001)
mas = []
mas = np.reshape(arr, (int(len(arr)/2), 2))
N = (mas.shape[0])
h = (b - a) / (N - 1)
result = trapezoidal(a, b, 2*N)
print('INTEGRAL = ', (result))
result_2 = trapezoidal(a, b, N)
print(((result_2-result)**2)**0.5, "= POGRESHNOST`")