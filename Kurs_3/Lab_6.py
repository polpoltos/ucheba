import numpy as np
import math
import matplotlib.pyplot as plt

c = [-4.3, -3.2, 0, 0]

A = [
    [-3.6, -8, 1, 0],
    [3.7, 8.1, 0, 1]
]

b = [-49.1, 59.1]
# c = [1, 0.3, 0, 0, 0, 0]
#
# A = [
#     [-34.6, -29.1, 1, 0, 0, 0],
#     [-6.4, 2.6, 0, 1, 0, 0],
#     [4.2, -2.4, 0, 0, 1, 0],
#     [5.2, 2.8, 0, 0, 0, 1],
# ]
#
# b = [-186.2, 13.6, 12.5, 36.9]
count_iters = 0

def f(x1, x2):
    return -4.3 * x1 + -3.2 * x2
# def f(x1, x2):
#     return 1 * x1 + 0.3 * x2


def simplex(c, A, b, iters):
    tableau = to_tableau(c, A, b)

    while can_be_improved(tableau):
        pivot_position = get_pivot_position(tableau)
        tableau = pivot_step(tableau, pivot_position)
        iters += 1

    return get_solution(tableau), iters


def to_tableau(c, A, b): #конвертируем исходные данные в таблицу
    xb = [eq + [x] for eq, x in zip(A, b)]
    z = c + [0]
    return xb + [z]


def can_be_improved(tableau): #проверка на оптимальность решения
    z = tableau[-1]
    print(z[:-1])
    return any(x > 0 for x in z[:-1])


def get_pivot_position(tableau):  #поиск опорного элемента
    z = tableau[-1]
    column = next(i for i, x in enumerate(z[:-1]) if x > 0)

    restrictions = []
    for eq in tableau[:-1]:
        el = eq[column]
        restrictions.append(math.inf if el <= 0 else eq[-1] / el)

    row = restrictions.index(min(restrictions))
    return row, column


def pivot_step(tableau, pivot_position):
    new_tableau = [[] for eq in tableau]

    i, j = pivot_position
    pivot_value = tableau[i][j]
    new_tableau[i] = np.array(tableau[i]) / pivot_value

    for eq_i, eq in enumerate(tableau):
        if eq_i != i:
            multiplier = np.array(new_tableau[i]) * tableau[eq_i][j]
            new_tableau[eq_i] = np.array(tableau[eq_i]) - multiplier
    print(new_tableau)
    return new_tableau


def is_basic(column):
    return sum(column) == 1 and len([c for c in column if c == 0]) == len(column) - 1


def get_solution(tableau):
    columns = np.array(tableau).T
    solutions = []
    for column in columns[:-1]:
        solution = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solution = columns[-1][one_index]
        solutions.append(solution)

    return solutions


x, iterations = simplex(c, A, b, count_iters)
func = f(x[0], x[1])
print("x1 =", round(x[0], 3), "\nx2 =", round(x[1], 3))
print("f(x) =", round(func, 3))
print("Количество итераций =", iterations+1)


# График
def plot_feasible_region(tableau, iteration):

    for i in range(len(A)):
        eq = A[i]
        b_value = b[i]
        plt.plot([-20, 20], [(b_value - eq[0] * (-20)) / eq[1], (b_value - eq[0] * 20) / eq[1]],
                 label=f'Ограничение {i + 1}')

    plt.scatter(x[0], x[1], color='red', marker='x', label='Оптимальное решение')

    current_solution = get_solution(tableau)
    plt.scatter(current_solution[0], current_solution[1], color='g', marker='o', label=f'Итерация {iteration}')
    plt.plot([0,0], [0,40], color="black")
    plt.plot([0, 20], [0,0], color="black")
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title(f'Итерация {iteration}')
    plt.legend()
    plt.grid(True)
    plt.show()


plot_feasible_region(to_tableau(c, A, b), 0)

tableau = to_tableau(c, A, b)
iteration = 1
while can_be_improved(tableau):
    pivot_position = get_pivot_position(tableau)
    tableau = pivot_step(tableau, pivot_position)
    plot_feasible_region(tableau, iteration)
    iteration += 1

plot_feasible_region(tableau, iteration)
