import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

# Задаем параметры задачи
k1, k2, k3, k4 = 10000, 20000, 50000, 500  # Константы скоростей реакций
E1, E2, E3, E4 = 156000, 166400, 177000, 160000  # Энергии активации (Дж/моль)
Q1, Q2, Q4 = 190000, 50000, 30000  # Теплоты реакций (Дж/моль)
Kt = 2000  # Теплопередача (Вт/м^2·К)
T_vx = 1200  # Температура на входе (К)
T_t = 500  # Температура стенок аппарата (К)
V = 10  # Объем реактора (м^3)
Ct = 1200  # Теплоемкость смеси (Дж/кг·К)
rho = 1.9  # Плотность (кг/м^3)
C_CH4_vx = 0.13  # Концентрация метана на входе
C_CH4_vx = C_CH4_vx * rho/(0.016)
C_NH3_vx = 0.12  # Концентрация аммиака на входе
C_NH3_vx = C_NH3_vx * rho/(0.017)
C_O2_vx = 0.15  # Концентрация кислорода на входе
C_O2_vx = C_O2_vx * rho/(0.032)
F_min, F_max = 5, 20  # Диапазон площадей теплообмена (м^2)
v_min, v_max = 0.01, 0.2  # Диапазон объемных расходов (м^3/с)
M0 = 15  # Начальная концентрация метана (моль/м^3)
K = 12  # Коэффициент теплопотерь

# Исходные условия
initial_conditions = [C_CH4_vx, C_NH3_vx, C_O2_vx, 0, 0, T_vx]  # CH4, NH3, O2, HCN, N2, T

# Дифференциальные уравнения
def reaction_model(t, y, F, v):
    CH4, NH3, O2, HCN, N2, T = y
    print(y)
    r1 = k1 * np.exp(-E1 / (8.314 * T)) * CH4 * O2**1.5  # Скорость первой реакции
    r2 = k2 * np.exp(-E2 / (8.314 * T)) * CH4            # Скорость второй реакции
    r3 = k3 * np.exp(-E3 / (8.314 * T)) * CH4 * O2      # Скорость третьей реакции
    r4 = k4 * np.exp(-E4 / (8.314 * T)) * NH3 * O2**1.5   # Скорость четвертой реакции

    # Уравнения для концентраций
    dCH4_dt = -r1 - r2 - r3
    dNH3_dt = -r4
    dO2_dt = -1.5 * r1 - r3 - 1.5 * r4
    dHCN_dt = r1
    dN2_dt = 0.5 * r4

    # Тепловой баланс
    Q_react = r1 * Q1 - r2 * Q2 + r4 * Q4
    dT_dt = (Q_react - Kt * F * (T - T_t)) / (rho * Ct * v)
    return [dCH4_dt, dNH3_dt, dO2_dt, dHCN_dt, dN2_dt, dT_dt]

# Целевая функция для оптимизации (отрицательная концентрация HCN на выходе)
def objective(params):
    F, v = params
    if not (F_min <= F <= F_max and v_min <= v <= v_max):
        return np.inf  # Штраф за выход за пределы диапазона
    solution = solve_ivp(reaction_model, [0, V / v], initial_conditions, args=(F, v))
    HCN_out = solution.y[3, -1]  # Концентрация HCN на выходе
    return -HCN_out  # Максимизация концентрации

# Начальное приближение
initial_guess = [10, 0.1]

# Границы параметров
bounds = [(F_min, F_max), (v_min, v_max)]

# Перезапустим оптимизацию с обновленным уравнением
result = minimize(objective, initial_guess, bounds=bounds, method='L-BFGS-B')


# Результаты
optimal_F, optimal_v = result.x
optimal_HCN = -result.fun

print(f"Оптимальная площадь теплообмена: {optimal_F} м^2")
print(f"Оптимальный объемный расход: {optimal_v} м^3/с")
print(f"Оптимальная концентрация HCN: {optimal_HCN:.10f} моль/м^3")
