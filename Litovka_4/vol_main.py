import matplotlib.pyplot as plt
import equation as eq
import numpy as np

A1 = 553
E1 = 48650
A2 = 2 * (10 ** 13)
E2 = 137000
D = 2.5
rho = 1400
C_hno3_in = 0.53
m_hno3_in = 7.5 # kg/s
m_nh3_in = 3 # kg/s
H = 0.5 # 0.5 <= H <= 10
T = 100 # 100 <= T <= 270 C

step = 0.1

def dC1dt(k1, C1, C2, tst, C1in):
    return ( (-1)*k1*C1*C2 + (1/tst)*(C1in-C1) )

def dC2dt(k1, C1, C2, tst, C2in):
    return ( (-1)*k1*C1*C2 + (1/tst)*(C2in-C2) )

def dc3dt(k1, k2, C1, C2, C3, tst):
    return ( k1*C1*C2 + (-1)*k2*C3 + (1/tst)*(0-C3) )

# def Calculate(T_cust, H_cust, t_len):
#     T_K = eq.Cel2Kel(Cels=T_cust)
#     _M = eq.M_calc(H=H_cust, D=D, rho=rho)
#     _k1 = eq.k1_calc(A1=A1, E1=E1, T=T_K)
#     _k2 = eq.k2_calc(A2=A2, E2=E2, T=T_K)
#     tSt = eq.tStay(M=_M, m_nh3=m_nh3_in, m_hno3=m_hno3_in*C_hno3_in)
#
#     c1 = [eq.C1_in(m_hno3=m_hno3_in, m_no3=m_nh3_in, C_hno3=C_hno3_in, rho=rho)]
#     c2 = [eq.C2_in(m_hno3=m_hno3_in, m_no3=m_nh3_in, C_hno3=C_hno3_in, rho=rho)]
#     c3 = [0]
#
#     t = [i for i in range(t_len)]
#     for i in t:
#         dc1 = dC1dt(k1=_k1, C1=c1[i], C1in=c1[0], C2=c2[i], tst=tSt)
#         dc2 = dC2dt(k1=_k1, C1=c1[i], C2=c2[i], tst=tSt, C2in=c2[0])
#         #dc3 = dc3dt(k1=_k1, k2=_k2, C1=c1[i], C2=c2[i], tst=tSt, C3=c3[i])
#         dc3 = dc3dt(k1=_k1, k2=_k2, C1=c1[i]+(dc1*step), C2=c2[i]+(dc2*step), tst=tSt, C3=c3[i])
#         c1.append(c1[i]+(dc1*step))
#         c2.append(c2[i]+(dc2*step))
#         c3.append(c3[i]+(dc3*step))
#         if abs(c3[i+1] - c3[i]) <= 0.000001 or c3[i+1] < 0:
#             break
#
#     # c1.pop()
#     # c2.pop()
#     # c3.pop()
#     #return c1, c2, c3, t
#     #print(f"rrrrr = {1 - (c3[len(c3)-1]*0.08/1400)}")
#     # print(T_cust ,T_K, H_cust)
#     # print(c3)
#     # print(c3[len(c3)-1]*0.08/1400)
#     return (c3[len(c3)-1]*0.08/1400)

def optCalc(T_cust, H_cust, arr_rand):
    T_K = T_cust#eq.Cel2Kel(Cels=T_cust)
    _M = eq.M_calc(H=H_cust, D=D, rho=rho)
    _k1 = eq.k1_calc(A1=A1, E1=E1, T=T_K)
    _k2 = eq.k2_calc(A2=A2, E2=E2, T=T_K)

    c3 = [0]
    count = 0
    for i in arr_rand:
        c1 = eq.C1_in(m_hno3=i, m_no3=m_nh3_in, C_hno3=C_hno3_in, rho=rho)
        c2 = eq.C2_in(m_hno3=i, m_no3=m_nh3_in, C_hno3=C_hno3_in, rho=rho)
        tSt = eq.tStay(M=_M, m_nh3=m_nh3_in, m_hno3=i * C_hno3_in)
        dc1 = dC1dt(k1=_k1, C1=c1, C1in=c1, C2=c2, tst=tSt)
        dc2 = dC2dt(k1=_k1, C1=c1, C2=c2, tst=tSt, C2in=c2)
        # dc3 = dc3dt(k1=_k1, k2=_k2, C1=c1[i], C2=c2[i], tst=tSt, C3=c3[i])
        dc3 = dc3dt(k1=_k1, k2=_k2, C1=c1 + (dc1 * step), C2=c2 + (dc2 * step), tst=tSt, C3=c3[count])
        c3.append(c3[count] + (dc3 * step))
        count += 1
    return c3

if __name__ == "__main__":
    # time = Calculate(T_cust=224, H_cust=5.6, t_len=60)
    # print(time)
    T_op = 438.934
    H_op = 10

    lines = []
    with open("randProc", 'r') as f:
        lines = f.read().split(' ')
    line2 = []
    for i in lines:
        if i != '':
            line2.append(float(i))
    print("rand")
    print(line2)

    C_res = optCalc(T_cust=T_op, H_cust=H_op, arr_rand=line2)
    c = []
    for i in C_res:
        c.append((1-i)*0.08/1400)
    print("C")
    print(c)
    t = [i for i in range(len(line2)+1)]
    print(t)
    plt.plot(t, c)
    plt.show()

    # H1, H2, H3, time = Calculate(T_cust=100, H_cust=3.59, t_len=600)
    # fig, (ax1, ax2, ax3) = plt.subplots(3)
    # print(H3[len(H3)-1]*0.08/1400*100)
    # ax1.plot(time, H1)
    # ax2.plot(time, H2)
    # ax3.plot(time, H3)
    # print(H1)
    # print(H2)
    # print(H3)
    # plt.show()