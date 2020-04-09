"""Functions that return the vapor pressure as a function of temperature
using NIST or IAPWS recommended equations"""


import numpy as np


def psat(T, unit='C', source='Wexler17'):
    """Return the vapor pressure (in Pascal) with given temperature


    Parameters
    ---------------------
    - T (float): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - source (str, default 'Simion') : Source for the used equation, (see 'Sources')
    
    Output
    - vapor pressure (in Pascal)
    
    Examples
    --------
    - psat(20) returns the vapor pressure of water at 20°C, using eq (17) of Wexler
    - psat(300, 'K', 'Wexler17') returns the value at 300K
    - psat(20, source='Wagner') returns the value at 20°C using Wagner equation


    Sources
    -------
    - Wexler and Greenspan : "Vapor Pressure Equation for Water in the Range 0 to 100°C"
    (1971). Valid from 0 to 100°C. Use 'Wexler17' or 'Wexler18' to compute with
    equation (17) or (18-c).
    - Bridgeman and Aldrich : "Vapor Pressure Tables for Water" (1964).
    Valid from 0 to 374.15°C.
    - Wagner and Pruß : "The IAPWS Formulation 1995 for the Thermodynamic Properties
    of Ordinary Water Substance for General and Scientific Use" (1995).
    Temperature validity seems to be 0 - 1000°C.
    """
    
    if unit == 'C':
        if not source == 'Bridgeman':
            T += 273.15
        else:
            pass
    elif unit == 'K':
        if source == 'Bridgeman':
            T -= 273.15
        else:
            pass
    else:
        raise ValueError(f'{unit} is not a valid unit')

    
    if source == 'Wexler17':
        if not 273.15 <= T <= 373.15:
            print('Warning : temperature outside of validity range (see "Source" in function doc)')
        else:
            E = [-7.51152e3, 9.65389644e1, 2.3998970e-2, -1.1654551e-5, -1.2810336e-8, 2.0998405e-11]
            B = -1.2150799e1
            
            p = B * np.log(T)
            for i in range(6):
                p += E[i] * T**(i-1)
            return np.exp(p)
    
    
    elif source == 'Wexler18':
        if not 273.15 <= T <= 373.15:
            print('Warning : temperature outside of validity range (see "Source" in function doc)')
        else:
            E = [-7.7847207e3, 1.1670432e2, 5.1177435e-2, -5.438695e-5, 3.189024e-8]
            B = -1.6463576e1
            
            p = B * np.log(T)
            for i in range(5):
                p += E[i] * T**(i-1)
            return np.exp(p)
    
    
    elif source == 'Bridgeman':
        if not 0 <= T <= 374.15:
            print('Warning : temperature outside of validity range (see "Source" in function doc)')
        else:
            A = 1.06423320; B = 1.0137921; C = 5.83531e-4; D = 4.16385282;
            E = 237.098157; F = 0.30231574; G = 3.377565e-3; H = 1.152894;
            K = 0.745794; L = 654.2906; M = 266.778
            
            Y1 = D*(T-187)/(T + E)
            X = 0.01 * (T - 187)
            Z = -1.87 + 3.74 * (H - K*np.arccosh(L/(T + M)))
            alpha = Z**2 * (1.87**2 - Z**2) / (F * (1 + G*T))
            Y2 = ( ((3*np.sqrt(3)) / (2*1.87**3)) * (X - 0.01*alpha) * (1.87**2 - (X - 0.01*alpha)**2) )/100
            
            p = A + Y1 - B*(1 + C*T)*Y2
            
            return (10**p)*101325


    elif source == 'Wagner':
        if not 273.15 <= T <= 1273.15:
            print('Warning : temperature outside of validity range (see "Source" in function doc)')
        else:    
            Pc = 22.064e6; Tc = 647.096; theta = 1 - T/Tc
            a1 = -7.85951783; a2 = 1.84408259; a3 = -11.7866497; a4 = 22.6807411;
            a5 = -15.9618719; a6 = 1.80122502
            
            val = Tc/T * (a1*theta + a2*theta**1.5 + a3*theta**3 + a4*theta**3.5 + a5*theta**4 + a6*theta**7.5)   
            p = np.exp(val)*Pc
            
            T -= 273.15
        
            return p
    else:
        raise ValueError(f'{source} is not a valid source (see Sources in function doc)')