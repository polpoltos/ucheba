import numpy as np
import matplotlib.pyplot as plt
import sympy
from scipy.optimize import fsolve

t0 = 0
t1 = 1
def equations(vars):
    x1, x2, x3 = vars
    eq1 = -126.0*x1 + 64.0*x2 + 64.25
    eq2 = 64.0*x1 - 126.0*x2 + 64.0*x3 + 0.5
    eq3 = 64.0 * x2 - 126.0 * x3 + 128.75
    return [eq1, eq2, eq3]
def function(t):
    return ((((2.5 - np.cos(np.sqrt(0.5)))*np.sin(t*np.sqrt(0.5)))/np.sin(np.sqrt(0.5))) + np.cos(t*np.sqrt(0.5)) - t/2)
# u0 = 1-2*((x1-1)/0.25)
# u1 = x1*0.25 + x1^2 -  2*((x2-x1)/0.25)
# u2 = x2*0.5 + x2^2 -  2*((x3-x2)/0.25)
# u3 = x3*0.75 + x3^2 -  2*((2-x3)/0.25)
x1, x2, x3 = sympy.symbols('x1 x2 x3')
u0 = 1-2*((x1-1)/0.25)**2
u1 = x1*0.25 + x1**2 - 2*((x2-x1)/0.25)**2
u2 = x2*0.5 + x2**2 - 2*((x3-x2)/0.25)**2
u3 = x3*0.75 + x3**2 - 2*((2-x3)/0.25)**2
urav = u0 + u1 + u2 + u3
print(sympy.diff(urav, 'x1'))
print(sympy.diff(urav, 'x2'))
print(sympy.diff(urav, 'x3'))
# Начальное предположение
initial_guess = [1, 1, 1]

# Решение системы уравнений
solution = list(fsolve(equations, initial_guess))
solution.insert(0, 1)
solution.append(2)
print(solution)
t_values = np.linspace(t0, t1, 40)
plt.plot(t_values, function(t_values), color='r', label='Решение Аналитическое',)
plt.plot([0, 0.25, 0.5, 0.75, 1],solution , '-o', label='Решение по методу', color='b')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('4x\'\' + 2x + t = 0')
plt.legend()
plt.show()