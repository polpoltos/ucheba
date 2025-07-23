import math


def M_calc(H, D, rho):
    return H * math.pi * D * rho

def _C2_in(m_hno3, m_no3, C_hno3):
    t1 = m_hno3 * C_hno3
    t2 = m_hno3 + m_no3
    return t1 / t2

def C2_in(m_hno3, m_no3, C_hno3, rho):
    c2_otn = _C2_in(m_hno3, m_no3, C_hno3)
    return (c2_otn * rho) / (63 * (10 ** -3))

def _C1_in(m_hno3, m_no3):
    t2 = m_hno3 + m_no3
    return m_no3 / t2

def C1_in(m_hno3, m_no3, C_hno3, rho):
    c1_otn = _C1_in(m_hno3, m_no3)
    return (c1_otn * rho) / (17 * (10 ** -3))

def k1_calc(A1, E1, T):
    R = 8.31
    return A1 * math.exp(-E1/(R * T))

def k2_calc(A2, E2, T):
    R = 8.31
    return A2 * math.exp(-E2/(R * T))

def Cel2Kel(Cels):
    return Cels + 273

def tStay(M, m_nh3, m_hno3):
    return M/(m_hno3 + m_nh3)