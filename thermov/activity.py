""" This module contains a function `a_w` that compute the water activity in a
Sodium Chloride solution as a function of concentration.
"""

import numpy as np
from thermov.conversions import convert
from thermov.ions import ion_magnitude

# ============================== Water activity ============================== 

def a_w(**kwargs):
    """Return water activity in function of a given concentration parameter.
    
    KWARGS
    - m= : molality (mol/kg)
    - w= : mass fraction
    - x= : mole fraction
        
    Output
    - Water activity
    
    Examples
    --------
    - a_w(x=0.1) returns water activity for a 0.1 mole fraction solution
    - a_w(m=6) returns water activity for a 6 molality solution
    - a_w(w=0.2) returns water activity for a 0.2 mass fraction solution

    Source
    -------
    - Clegg et al. : "Thermodynamic Properties of Aqueous Aerosols to High
    Supersaturation: II" (1997). Valid at 25°C and for solutions of molality
    up to ~17
    """
    
    for key, value in kwargs.items():
        if key == 'x':
            x_NaCl = value # mole fraction of NaCl
        elif key == 'w':
            x_NaCl = convert(value, 'w', 'x') # mole fraction in function of mass fraction
        elif key == 'm': 
            x_NaCl = convert(value, 'm', 'x') # mole fraction in function of molality
        else:
            raise ValueError('Concentration parameter can be m, w or x')

    if (type(x_NaCl) == float or type(x_NaCl) == int) and not 0 <= x_NaCl <= 0.233:
        print('Warning :  concentration outside of validity range for activity (0 <= m <~ 17)')            
    if type(x_NaCl) == np.ndarray and not all(0 <= x <= 0.233 for x in x_NaCl):
        print('Warning : some concentrations outside of validity range for activity (0 <= m <~ 17)')
        
    x_Cl = x_NaCl / (1 + x_NaCl) # mole fraction of Cl
    x_Na = x_NaCl / (1 + x_NaCl) # mole fraction of Na
    x1 = 1 - (x_Na + x_Cl) # mole fraction of water
    
    z_Cl = ion_magnitude['Cl']
    
    I = convert(x_NaCl, 'x', 'I') #ionic strength
    
    rho = 13.0
    
    A_x = 2.915  # could be A_x(T)
    B = 24.22023
    alpha = 5.0
    W1 = 0.7945378
    U1 = 12.15304
    V1 = -12.76357
    
    val = 2 * A_x * I**(3 / 2) / (1 + rho * I**(1 / 2)) #1st line    
    val -= x_Na * x_Cl * B * np.exp(-alpha * I**(1 / 2)) #2nd line    
    val += (1 - x1) * x_Cl * (1 +  z_Cl) * W1  #5th line    
    val += (1 - 2 * x1) * x_Na * x_Cl * ((1 +  z_Cl)**2 / z_Cl) * U1 #6-7th lines    
    val += 4 * x1 * (2 - 3 * x1) * x_Na * x_Cl * V1 #8th line
    
    f1 = np.exp(val)    
    a1 = f1 * x1
   
    return a1
