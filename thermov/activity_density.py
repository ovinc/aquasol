""" This module contains functions that compute some thermodynamic quantities
in Sodium Chloride solution :
    - `a_w` returns the water activity
    - `rho` and `rho2` returns the density of the solution 
"""

import numpy as np

# ============================== Water activity ============================== 

def a_w(**kwargs):
    """Return water activity in function of a given concentration parameter.
    
    Uses eq (6) of Clegg et al. 1997 (valid from molality equal to 0 up to ~17)
    Activity can either be calculated in function of molality m, mass fraction w
    or mole fraction x ( e.g. a_w(m = 6) )
    """
        
    M_w = 18.01528e-3 # molar mass of water, kg/mol
    M_NaCl = 58.443e-3 # molar mass of NaCl, kg/mol
    
    for key, value in kwargs.items():
        if key == 'x':
            x_NaCl = value # mole fraction of NaCl
        elif key == 'w':
            x_NaCl = value / (M_NaCl * (value / M_NaCl + (1 - value) / M_w)) # mole fraction in function of mass fraction
        elif key == 'm': 
            x_NaCl = (value * M_w) / (value * M_w + 1) # mole fraction in function of molality
        
        
    x_Cl = x_NaCl / (1 + x_NaCl) # mole fraction of Cl
    x_Na = x_NaCl / (1 + x_NaCl) # mole fraction of Na
    x1 = 1 - (x_Na + x_Cl) # mole fraction of water
    
    z_Cl = 1.0 #magnitude of the charge of the ion
    I_x = 0.5 * (x_Na + x_Cl) #ionic strength
    rho = 13.0
    
    A_x = 2.915  # could be A_x(T)
    B = 24.22023
    alpha = 5.0
    W1 = 0.7945378
    U1 = 12.15304
    V1 = -12.76357
    
    val = 2 * A_x * I_x**(3 / 2) / (1 + rho * I_x**(1 / 2)) #1st line    
    val -= x_Na * x_Cl * B * np.exp(-alpha * I_x**(1 / 2)) #2nd line    
    val += (1 - x1) * x_Cl * (1 + z_Cl) * W1  #5th line    
    val += (1 - 2 * x1) * x_Na * x_Cl * ((1 + z_Cl)**2 / z_Cl) * U1 #6-7th lines    
    val += 4 * x1 * (2 - 3 * x1) * x_Na * x_Cl * V1 #8th line
    
    f1 = np.exp(val)    
    a1 = f1 * x1
    
    return a1


# ============================= Solution density =============================

def rho(w, T, relative_density=False):
    """Return the density of sodium chloride solution (up to saturation)
    
    Uses equation (3) of Simion et al. 2015 (valid from 0 to 26% and from 0 to 100 °C)
    
    INPUTS
    - mass fraction
    - temperature (in °Celsius)
    - relative_density : False (default) to return density in kg/m³
    True for relative density
    
    OUTPUT
    - Volumic mass or density
    """
    w = w * 100
    T = T +273.15
    a1 = 750.2834; a2 = 26.7822; a3 = -0.26389
    a4 = 1.90165; a5 = -0.11734; a6 = 0.00175
    a7 = -0.003604; a8 = 0.0001701; a9 = -0.00000261
    rho = (a1 + a2 * w + a3 * w**2) + (a4 + a5 * w + a6 * w**2) * T + (a7 + a8 * w + a9 * w**2) * T**2
    if relative_density == False:
        return rho
    if relative_density == True:
        return rho/1000
    

def rho2(w, relative_density=False):
    """Return the density of sodium chloride solution at 25°C.
    
    Uses equation (5) of Tang 1996 (valid from from w = 0 to w ~= 80)
    
    INPUTS
    - Mass fraction (between 0 and 1)
    - relative_density : False (default) to return density in kg/m³,
      True for relative density
    
    OUTPUT
    - Relative density or density
    """
    w = w * 100
    rho = 0.9971
    A = [7.41e-3, -3.741e-5,2.252e-6, -2.06e-8]
    for i in range(4):
        rho += A[i] * w**(i+1)
    if relative_density == False:
        return rho*1000
    if relative_density == True:
        return rho
