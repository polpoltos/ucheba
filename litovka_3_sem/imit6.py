import math
import numpy as np
import matplotlib.pyplot as plt

l1 = 11
l2 = 7
M0 = 15
sigma0 = 12
a = 0.1
N = 200
Zi = 200
Ns = 10
Kz = 20

def M_ogid(x_s, n):
    return (1/n)*np.sum(x_s)

def sigma(z, M, n):
    sig = 0
    for i in range(n):
        sig+=(z[i] - M)**2
    return (1/n)*sig

def rand(xi, sg):
    z = []
    i_s = []
    for i in range(N): z.append(0)
    param1 = 1/Ns
    param2 = 0
    for i in range(N):
        param2=0
        for j in range(i, i+Ns):
            param3 = math.sqrt((sigma0/(sg*a)) * math.e**(-a*(j-i)))
            param2 += xi[j]*param3
        z[i] = param1 * param2 + M0
        i_s.append(i)
        z_s = z.copy()
        z_s.append(param1*param2)
    return z, i_s, z_s

def corr(Mz):
    k = []
    S = []
    for i in range(0, Kz):
        par = 0
        S.append(i)
        for j in range(1, Zi - i):
            par += (Z_i_s[j] - Mz) * (Z_i_s[j + i] - Mz)
        par20 = 1 / (Zi - i)
        k.append(par20 * par)
    return k, S

def approx(k, s, sig):
    alph = []
    for i in range(len(s)):
        alp_def = 1
        kt = sig * math.exp(-alp_def * abs(s[i]))
        while kt < abs(k[i]):
            alp_def -= 0.01
            kt = sig * math.exp(-alp_def * abs(s[i]))
        alph.append(alp_def)
    al = 0
    for i in alph:
        al += i

    alpFin = al/len(alph)
    kApr = []
    for i in range(len(s)):
        kApr.append(sig * math.exp(-alpFin * abs(s[i])))
    return alpFin, kApr


def generator(n):
    del1 = l1**0.5
    del2 = l2 ** 0.5
    x = [(del1 % 1)-0.5]
    ia = [0]
    for i in range(n-1):
        x.append(((del2*x[i-1])%1)-0.5)
        ia.append(i)
    return x, ia

plt.figure(figsize=(14, 5))


X_i, I_s = generator(N+10)
M_x = M_ogid(X_i, N+10)
Sigma_2 = sigma(X_i, M_x, N+10)
plt.subplot(1, 1, 1).set_title('Концентрация метана на входе')

Z_i, I_s, Z_i_s = rand(X_i, Sigma_2)
M_z = M_ogid(Z_i_s, len(Z_i_s))
Sigma_2_z = sigma(Z_i_s, M_z, N+1)
print(Z_i_s)
plt.plot(I_s, Z_i)
plt.grid()
K_p, S_p = corr(M_z)
alfa, K_aprox = approx(K_p, S_p, Sigma_2_z)
plt.grid()
plt.show()
