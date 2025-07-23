import numpy as np
import matplotlib.pyplot as plt


A = 1.3*10**(-1)
Delta_X = 0.1
X = 1
Tau_Max = 100
del_t = 0.5 * Delta_X ** 2

def function_fiX(x):
    return 30+x

def function_f1(t):
    return 50

def function_f2(t):
    return 50

def plotCreator():
    time = np.arange(0,Tau_Max+del_t,del_t)
    L = np.arange(0,X+Delta_X,Delta_X)
    T = np.array([[0.1 for i in np.arange(len(L))] for _ in np.arange(len(time))])
    for i in range(0,X*10+1,1):
        T[0][i] = function_fiX(i/10)
    for j in np.arange(0, len(time) - 1):
        T[j+1][0] = function_f1(time[j])
        for i in np.arange(1, 10):
            T[j+1][i] = T[j][i] + (((A * del_t)/Delta_X**2)*(T[j][i + 1] - 2 * T[j][i] + T[j][i-1]))
        T[j+1][-1]=function_f2(time[j])
    print(T[0])
    L, time = np.meshgrid(L, time)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(L, time, T, c='r', marker='x')

    ax.set_xlabel('l')
    ax.set_ylabel('Tau')
    ax.set_zlabel('T')

    plt.show()

if __name__ == '__main__':
    plotCreator()