import numpy as np
from scipy.integrate import solve_ivp

k1, k2, k3, k4 = 10000, 20000, 50000, 500
E1, E2, E3, E4 = 156000, 166400, 177000, 160000
Q1, Q2, Q4 = 190000, 50000, 30000
Kt = 2000
T_vx = 1200
T_t = 500
V = 10
Ct = 1200
rho = 1.9
C_CH4_vx = 0.13 * rho / 0.016
C_NH3_vx = 0.12 * rho / 0.017
C_O2_vx = 0.15 * rho / 0.032
F_min, F_max = 5, 20
v_min, v_max = 0.01, 0.2
M0 = 15
K = 12

initial_conditions = [C_CH4_vx, C_NH3_vx, C_O2_vx, 0, 0, T_vx]

def reaction_model(t, y, F, v):
    CH4, NH3, O2, HCN, N2, T = y
    r1 = k1 * np.exp(-E1 / (8.314 * T)) * CH4 * O2**1.5
    r2 = k2 * np.exp(-E2 / (8.314 * T)) * CH4
    r3 = k3 * np.exp(-E3 / (8.314 * T)) * CH4 * O2
    r4 = k4 * np.exp(-E4 / (8.314 * T)) * NH3 * O2**1.5

    dCH4_dt = -r1 - r2 - r3
    dNH3_dt = -r4
    dO2_dt = -1.5 * r1 - r3 - 1.5 * r4
    dHCN_dt = r1
    dN2_dt = 0.5 * r4

    Q_react = r1 * Q1 - r2 * Q2 + r4 * Q4
    dT_dt = (Q_react - Kt * F * (T - T_t)) / (rho * Ct * v)

    return [dCH4_dt, dNH3_dt, dO2_dt, dHCN_dt, dN2_dt, dT_dt]

def penalty_function(params):
    F, v = params
    penalty = 0

    if not (F_min <= F <= F_max):
        penalty += (F - F_max) ** 2 if F > F_max else (F_min - F) ** 2

    if not (v_min <= v <= v_max):
        penalty += (v - v_max) ** 2 if v > v_max else (v_min - v) ** 2

    return penalty

def objective_with_penalty(params):
    F, v = params
    penalty = penalty_function(params)

    solution = solve_ivp(reaction_model, [0, V / v], initial_conditions, args=(F, v))
    HCN_out = solution.y[3, -1]
    return -HCN_out + penalty

def optimize_with_penalty_method():
    current_params = [10, 0.1]
    learning_rate = 0.01
    num_iterations = 1000
    tolerance = 1e-6

    for _ in range(num_iterations):
        grad = np.zeros_like(current_params)
        for i in range(len(current_params)):
            step = np.zeros_like(current_params)
            step[i] = learning_rate
            loss_plus = objective_with_penalty(current_params + step)
            loss_minus = objective_with_penalty(current_params - step)
            grad[i] = (loss_plus - loss_minus) / (2 * learning_rate)
        new_params = current_params - learning_rate * grad

        if np.linalg.norm(new_params - current_params) < tolerance:
            break

        current_params = new_params

    return current_params

optimal_params = optimize_with_penalty_method()
optimal_F, optimal_v = optimal_params
optimal_HCN = -objective_with_penalty(optimal_params)

print(f"Оптимальная площадь теплообмена: {optimal_F} м^2")
print(f"Оптимальный объемный расход: {optimal_v} м^3/с")
print(f"Оптимальная концентрация HCN: {optimal_HCN:.10f} моль/м^3")
