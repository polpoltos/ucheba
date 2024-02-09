import numpy as np
import matplotlib.pyplot as plt


def function(t):
    return ((((2.5 - np.cos(np.sqrt(0.5)))*np.sin(t*np.sqrt(0.5)))/np.sin(np.sqrt(0.5))) + np.cos(t*np.sqrt(0.5)) - t/2)

def shooting_method(f, a, b, N, alpha):
    h = (b - a) / N
    t = a
    w = np.zeros((N+1, len(alpha)))
    w[0] = alpha
    for i in range(N):
        w[i+1] = w[i] + h * f(t, w[i])
        t = a + i*h
    return w

def f(t, v):
    x = v[0]
    y = v[1]
    fx = y
    fy = -(2*x + t) / 4
    return np.array([fx, fy])

def main():
    a = 0
    b = 1
    N = 40
    alpha = 1
    h = 0.01

    initial_slope = 1
    result = shooting_method(f, a, b, N, np.array([alpha, initial_slope]))
    print(result[:, 0][-1])
    res = result[:, 0][-1]
    otv = 0
    while True:
        if res < function(b):
            initial_slope += h
            otv = shooting_method(f, a, b, N, np.array([alpha, initial_slope]))
        else:
            initial_slope -= h
            otv = shooting_method(f, a, b, N, np.array([alpha, initial_slope]))
        if abs(function(b) - otv[:, 0][-1]) <= 0.02:
            result = otv
            break
    print(result[:, 0][-1])
    print(f'Угловой коэффициент = {initial_slope}')

    # Plot the solution
    t_values = np.linspace(a, b, N+1)
    x_values = result[:, 0]
    plt.plot(t_values, function(t_values), color='r', label='Решение Аналитическое',)
    plt.plot(t_values, x_values, '-o', label='Решение по методу', color='b')
    plt.xlabel('t')
    plt.ylabel('x(t)')
    plt.title('4x\'\' + 2x + t = 0')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
