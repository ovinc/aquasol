""" This module contains a function `density` that compute Sodium Chloride
solution density
"""

# TODO - Check how validity range depends on temperature (e.g. for Simion)
# TODO - Add tests

import numpy as np
from thermov.conversions import convert


def density(T=25, unit='C', relative=False, solute=None, source='Simion', **kwargs):
    """Return the density of sodium chloride solution.
    
    Parameters
    ---------------------
    - T (float): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - relative (bool, default False): True for relative density
    - solute: None at the moment.
    - source (str, default 'Simion') : Source for the used equation,
    can be 'Simion' or 'Tang' (see 'Sources')

    KWARGS
    - m= : molality (mol/kg)
    - w= : mass fraction
    - x= : mole fraction
    
    Output
    - density or relative density
    
    
    Examples
    --------
    - density(w=0.1) returns the density calculated with Simion equation
    for a mass fraction of 0.1
    - density(300, 'K', m=6) returns the value at 300K for a molality of 6
    - density(source='Tang', x=0.1) returns the value calculated with Tang
    equation for a mole fraction of 0.1


    Sources
    -------
    - Simion et al. (default) : "Mathematical modelling of density and
    viscosity of NaCl aqueous solutions" (2015). Valid from w = 0 to w = 0.26
    and for temperatures between 0 and 100°C

    - Tang : "Chemical and size effects of hygroscopic aerosols on light
    scattering coefficients" (1996). Valid at 25°C and from w = 0 to w ~= 0.8
    """
    if unit == 'C':
        T += 273.15
    elif unit == 'K':
        pass
    else:
        raise ValueError(f'{unit} is not a valid unit')
    
    for key, value in kwargs.items():
        if key == 'w':
            w_NaCl = value # mass fraction of NaCl
        elif key == 'x':
            w_NaCl = convert(value, 'x', 'w') # mass fraction in function of mole fraction
        elif key == 'm': 
            w_NaCl = convert(value, 'm', 'w') # mass fraction in function of molality
        else:
            raise ValueError('Concentration parameter can be w for mass fraction, x for mole fraction or m for molality')
            
    w = w_NaCl * 100
    
    if source == 'Simion':
        if (type(w) == float or type(w) == int) and not 0 <= w <= 26:
            print('Warning : concentration outside of validity range for density (0 <= w <= 0.26 for Simion)')
        elif type(w) == np.ndarray and not all(0 <= W <= 26 for W in w):
            print('Warning : concentration(s) outside of validity range for density (0 <= w <= 0.26 for Simion)')
        if not 273.15 <= T <= 373.15:
            print('Warning : temperature outside of validity range for density (0 - 100°C for Simion)')
        
        a1 = 750.2834; a2 = 26.7822; a3 = -0.26389
        a4 = 1.90165; a5 = -0.11734; a6 = 0.00175
        a7 = -0.003604; a8 = 0.0001701; a9 = -0.00000261
        rho = (a1 + a2 * w + a3 * w**2) + (a4 + a5 * w + a6 * w**2) * T + (a7 + a8 * w + a9 * w**2) * T**2
        if relative == False:
            return rho
        if relative == True:
            return rho/1000
        
    elif source == 'Tang':
        if (type(w) == float or type(w) == int) and not 0 <= w <= 80:
            print('Warning : concentration outside of validity range for density (0 <= w <~ 0.8 for Tang)')
        elif type(w) == np.ndarray and not all(0 <= W <= 80 for W in w):
            print('Warning : some concentration outside of validity range for density (0 <= w <~ 0.8 for Tang)')
        if not T == 298.15:
            print('Warning : Tang is just for density at 25°C')
        
        rho = 0.9971
        A = [7.41e-3, -3.741e-5,2.252e-6, -2.06e-8]
        for i in range(4):
            rho += A[i] * w**(i+1)
        if relative == False:
            return rho*1000
        if relative == True:
            return rho

    else:
        raise ValueError('Source can either be "Simion" or "Tang"')