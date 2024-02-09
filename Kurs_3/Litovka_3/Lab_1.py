import numpy as np
import matplotlib.pyplot as plt


def function(x):
    return x**3 - 4.5*x**2 + 6*x - 12

def fib(n):
    a = 0
    b = 1
    for __ in range(n):
        a, b = b, a + b
    return a

def number(a, b):
    n = 1
    counter = 0
    while (abs(b-a) / 0.01) > n:
        n = fib(counter)
        counter += 1
    return counter


def delenia(a, b):
    y_a = function(a)
    y_b = function(b)
    counter = 0
    while (b - a) > 0.1:
        x = [a, a + 0.25 * (b - a), b - 0.25 * (b - a), b]
        y = [y_a, function(x[1]), function(x[2]), y_b]
        print(x)
        print(y)
        if y.index(min(y)) <= 1:
            a = x[0]
            b = x[2]
            y_b = y[2]
        else:
            a = x[1]
            b = x[3]
            y_a = y[1]
        counter += 1
        print(f"x = {x[y.index(min(y))]} y = {min(y)}")
    print(f"Количество итерация методом половинного деления равно: {counter}")
def gold(a, b):
    y_a = function(a)
    y_b = function(b)
    counter = 0
    while (b - a) > 0.1:
        x = [a, a + 0.38 * (b - a), b - 0.38 * (b - a), b]
        y = [y_a, function(x[1]), function(x[2]), y_b]
        print(x)
        print(y)
        if y.index(min(y)) <= 1:
            a = x[0]
            b = x[2]
            y_b = y[2]
        else:
            a = x[1]
            b = x[3]
            y_a = y[1]
        print(f"x = {x[y.index(min(y))]} y = {min(y)}")
        counter += 1
    print(f"Количество итерация методом Золотого сечения: равно: {counter}")

def fibon(a, b):
    k = 1
    y_a = function(a)
    y_b = function(b)
    n = number(a, b)
    print(n)
    x1 = b - fib(n - 1) / fib(n) * (b - a)
    x2 = a + fib(n - 1) / fib(n) * (b - a)
    while (x2 - x1) > 0.1:
        x = [a, x1, x2, b]
        print(f"x = {x}")
        y = [function(a), function(x1), function(x2), function(b)]
        print(f"f(x) = {y}")
        print(min(y))
        if y.index(min(y)) <= 1:
            a = x[0]
            b = x[2]
            x2 = x1
            x1 = b - fib(n - k) / fib(n - k + 1) * (b - a)
        else:
            a = x[1]
            b = x[3]
            x1 = x2
            x2 = a + fib(n - k) / fib(n - k + 1) * (b - a)
        k += 1
    print(f"x = {x[y.index(min(y))]} y = {min(y)}")
    print(f"Количество итераций методом Фиббоначи: {k}")

a = 0
b = 1.5
delenia(a, b)
gold(a,b)
fibon(a,b)

spisok_x = []
for i in range(16):
    spisok_x.append(round(a, 1))
    a+=0.1
spisok_y = list(map(function, spisok_x))
plt.figure(figsize=(10, 5))
plt.plot(spisok_x, spisok_y)
plt.xlabel(r'$x$')
plt.ylabel(r'$f(x)$')
plt.grid(True)
plt.show()