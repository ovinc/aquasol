import numpy as np


def psat0(T):
    """
    Returns the vapor pressure (in Pascal) with given temperature (in ° Celsius)
    using eq(17) of Wexler and Greenspan 1971 (Valid from 0 to 100 °C)
    """
    T += 273.15
    E = [-7.51152e3, 9.65389644e1, 2.3998970e-2, -1.1654551e-5, -1.2810336e-8, 2.0998405e-11]
    B = -1.2150799e1
    
    p = B * np.log(T)
    for i in range(6):
        p += E[i] * T**(i-1)
    return np.exp(p)
    
    
def psat1(T):
    """
    Returns the vapor pressure (in Pascal) with given temperature (in ° Celsius)
    using eq(18c) of Wexler and Greenspan 1971 (Valid from 0 to 100 °C)
    """
    T += 273.15
    E = [-7.7847207e3, 1.1670432e2, 5.1177435e-2, -5.438695e-5, 3.189024e-8]
    B = -1.6463576e1
    
    p = B * np.log(T)
    for i in range(5):
        p += E[i] * T**(i-1)
    return np.exp(p)




def psat2(T):
    """
    Returns the vapor pressure (in Pascal) with given temperature (in ° Celsius)
    using the equation developped by Bridgeman and Aldrich in 1964 (Valid from 0 to 374.15 °C)
    """
    A = 1.06423320; B = 1.0137921; C = 5.83531e-4; D = 4.16385282; E = 237.098157
    F = 0.30231574; G = 3.377565e-3; H = 1.152894; K = 0.745794; L = 654.2906; M = 266.778
    
    Y1 = D*(T-187)/(T + E)
    X = 0.01 * (T - 187)
    Z = -1.87 + 3.74 * (H - K*np.arccosh(L/(T + M)))
    alpha = Z**2 * (1.87**2 - Z**2) / (F * (1 + G*T))
    Y2 = ( ((3*np.sqrt(3)) / (2*1.87**3)) * (X - 0.01*alpha) * (1.87**2 - (X - 0.01*alpha)**2) )/100
    
    p = A + Y1 - B*(1 + C*T)*Y2
    
    return (10**p)*101325
    

print(psat0(20))
print(psat1(20))
print(psat2(20))

    
    
    
