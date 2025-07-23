import math
import matplotlib.pyplot as plt
import numpy as np



N = 200 + 10 # Р”Р»РёРЅР° СЂСЏР»Р° СЃР»СѓС‡ С‡РёСЃРµР» xi
Zi = 200
Kz = 20
Ns = 10
# РјРµС‚РѕРґ РёСЂСЂР°С†РёРѕРЅР°Р»СЊРЅС‹С… С‡РёСЃРµР»
Delt1 = math.sqrt(11)
Delt2 = math.sqrt(13)
M0 = 7.5
Sig0pow2 = 1.6
Alph0 = 0.082

def generatorIrrationalMethod(n,Del1, Del2):
    x = [(Del1 % 1)-0.5]
    ia = [0]
    for i in range(n-1):
        x.append(((Del2*x[i-1])%1)-0.5)
        ia.append(i)
    plt.plot(ia, x)
    plt.title("IrrationalMethod")
    plt.xlabel("N")
    plt.ylabel("X")
    plt.show()
    #print(len(x))
    return x
def mCalc(x_arr, N):    # 1.35
    sum = 0
    for i in x_arr:
        sum += i
    M = (1/N) * sum
    return M
def sigCalc(x_arr, N, M):   # 1.36
    sum = 0
    for i in x_arr:
        sum += (i - M)**2
    sig = (1/N) * sum
    return sig
def randProcessGen(): # 1.41
    z = []
    ia = []
    for i in range(Zi): z.append(0)

    par1 = 1 / Ns
    par2 = 0
    for i in range(Zi):
        par2 = 0
        for j in range(i, i+Ns):
            par3 = math.sqrt((Sig0pow2/(Sg2*Alph0)) * math.e**(-Alph0*(j-i)))
            par2 += xi[j] * par3
        z[i] = par1*par2 + M0
        ia.append(i)
    plt.plot(ia, z)
    plt.title("РџСЂРѕС†РµСЃСЃ")
    plt.xlabel("N")
    plt.ylabel("Z")
    plt.show()
    z.append(par1*par2)
   # print(z)
   # print(len(z))
    return z
def correlationFunction(): # 1.37
    k = []
    S = []
    for i in range(0, Kz):
        par = 0
        S.append(i)
        for j in range(1, Zi-i):
            par += (zi[j] - Mz)*(zi[j+i] - Mz)
        par20 = 1/(Zi-i)
        k.append(par20*par)
   # print(k)
   # print(S)
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

xi = generatorIrrationalMethod(N, Delt1, Delt2)
Mx = mCalc(xi, N)
Sg2 = sigCalc(xi, N, Mx)
print(f"РЎР»СѓС‡Р°Р№РЅС‹Рµ С‡РёСЃР»Р°: {xi}")
print(f"РњР°С‚РµРјР°С‚РёС‡РµСЃРєРѕРµ РѕР¶РёРґР°РЅРёРµ: {Mx}")
print(f"Р”РёСЃРїРµСЂСЃРёСЏ: {Sg2}")

zi = randProcessGen()
Mz = mCalc(zi, Zi)
zSg2 = sigCalc(zi, Zi, Mz)
print(f"РЎР»СѓС‡Р°Р№РЅС‹Р№ РїСЂРѕС†РµСЃСЃ: {zi}")
with open("randProc", 'w') as f:
    for i in zi:
        f.write(str(i) + ' ')
print(f"РњР°С‚РµРјР°С‚РёС‡РµСЃРєРѕРµ РѕР¶РёРґР°РЅРёРµ z: {Mz}")
print(f"Р”РёСЃРїРµСЂСЃРёСЏ z: {zSg2}")
print(f"РњР°С‚РµРјР°С‚РёС‡РµСЃРєРѕРµ РѕР¶РёРґР°РЅРёРµ 0: {M0}")
print(f"Р”РёСЃРїРµСЂСЃРёСЏ 0: {Sig0pow2}")

Kp, Sp =correlationFunction()
alpha_calc, Kapr = approx(Kp, Sp, zSg2)
print(f"Р Р°СЃС‡РµС‚РЅР°СЏ Р°Р»СЊС„Р°: {alpha_calc}")
print(f"РђР»СЊС„Р° 0: {Alph0}")
plt.plot(Sp, Kapr, 'g')
plt.plot(Sp, Kp, "b")
plt.title("Approx")
plt.xlabel("S")
plt.ylabel("K")
plt.show()