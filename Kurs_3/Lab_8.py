import numpy as np
import matplotlib.pyplot as plt


t0 = 0
t1 = 1
A = [1, 2, 4]
def function(t):
    return ((((2.5 - np.cos(np.sqrt(0.5)))*np.sin(t*np.sqrt(0.5)))/np.sin(np.sqrt(0.5))) + np.cos(t*np.sqrt(0.5)) - t/2)


def Wi(t, A):
    return (A[0] * t**2 + A[1]*t**4)/ (A[2]*t**3)**0.5

def W0(t):
    return t + 1

def Kantarovich(t, A):
    return W0(t) + (t - t0)*(t - t1)*Wi(t, A)

while True:
    if Kantarovich(0.5, A) > function(0.5):
        for i in range(len(A)):
            A[i] += 0.02
    else:
        for i in range(len(A)):
            A[i] -= 0.02
    if abs(Kantarovich(0.5, A) - function(0.5)) < 0.01:
        break
print(A)
t_values = np.linspace(t0, t1, 40)
plt.plot(t_values, function(t_values), color='r', label='Решение Аналитическое',)
plt.plot(t_values, Kantarovich(t_values, A), '-o', label='Решение по методу', color='b')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('4x\'\' + 2x + t = 0')
plt.legend()
plt.show()