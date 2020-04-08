""" This module contains functions that compute some thermodynamic quantities
in Sodium Chloride solution :
    - `a_w` returns the water activity
    - `rho` and `rho2` returns the density of the solution 
"""

# TODO - Give warning when parameterr (e.g. mass fraction) outside of validity range
# TODO - Check how validity range depends on temperature (e.g. for Simion)
# TODO - Add tests
# TODO -- continue rewriting code in the format I have started for the arguments
# (and have single function with different sources)

import numpy as np

# ============================== Water activity ============================== 


def density(T=20, unit='C', relative=False, solute=None, **kwargs):
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
