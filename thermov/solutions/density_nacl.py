"""Gathers the formulas for the density of NaCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns two parameters:
- rho, density in kg / m^3
- rho0, density of pure water
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
- Simion et al. (default) : "Mathematical modelling of density and
viscosity of NaCl aqueous solutions" (2015). Valid from w = 0 to w = 0.26
and for temperatures between 0 and 100°C

- Tang : "Chemical and size effects of hygroscopic aerosols on light
scattering coefficients" (1996). Valid at 25°C and from w = 0 to w ~= 0.5
"""

import numpy as np

# General Info about the formulas 
sources = ['Simion', 'Tang']
default_source = 'Simion'

concentration_types = {'Simion': 'w',
                       'Tang': 'w',
                       }

concentration_ranges = {'Simion': (0, 0.26),
                        'Tang': (0, 0.5),
                        } 

temperature_units = {'Simion': 'C',
                     'Tang': 'C',
                     }
                     
temperature_ranges = {'Simion': (0, 100),
                      'Tang': (25, 25),
                      }

# ============================== FORMULAS ==================================== 

def density_simion(w, T):

    w = w * 100  # avoid using *= to not mutate objects in place
    T = T + 273.15  # same
        
    a1 = 750.2834; a2 = 26.7822; a3 = -0.26389
    a4 = 1.90165; a5 = -0.11734; a6 = 0.00175
    a7 = -0.003604; a8 = 0.0001701; a9 = -0.00000261

    rho0 = a1 + a4*T + a7*T**2  # density of pure water
    rho = rho0 + a2*w + a3*w**2 + (a5*w + a6*w**2) * T + (a8*w + a9*w**2) * T**2

    return rho, rho0


def density_tang(w, T):

    w = w * 100
    
    rho0 = 997.1  # density of pure water (at 25°C)
    rho = rho0
    A = np.array([7.41e-3, -3.741e-5,2.252e-6, -2.06e-8])*1000
    for i, a in enumerate(A):
        rho += a * w**(i+1)

    return rho, rho0


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {'Simion': density_simion,
            'Tang': density_tang,
            }