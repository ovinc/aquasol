"""Gathers the formulas for the density of NaCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns two parameters:
- rho0, density of pure water in kg / m^3
- rho, density of solution in kg / m^3
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
- Simion (default) : "Mathematical modelling of density and
viscosity of NaCl aqueous solutions" (2015). Valid from w = 0 to w = 0.26
and for temperatures between 0 and 100°C

- Tang: "Chemical and size effects of hygroscopic aerosols on light
scattering coefficients" (1996). Valid at 25°C and from w = 0 to w ~= 0.5

- Al Ghafri et al., Densities of Aqueous MgCl 2 (aq), CaCl 2 (aq), KI(aq),
NaCl(aq), KCl(aq), AlCl 3 (aq), and (0.964 NaCl + 0.136 KCl)(aq) at
Temperatures Between (283 and 472) K, Pressures up to 68.5 MPa, and
Molalities up to 6 mol·kg −1.
Journal of Chemical & Engineering Data 57, 1288-1304 (2012).
"""

import numpy as np

from .misc import rho_alghafri
from thermov.water import density_atm

# General Info about the formulas

default_source = 'Simion'

concentration_types = {'Simion': 'w',
                       'Tang': 'w',
                       'Al Ghafri': 'm'
                       }

concentration_ranges = {'Simion': (0, 0.26),
                        'Tang': (0, 0.5),
                        'Al Ghafri': (0, 6)
                        }

temperature_units = {'Simion': 'C',
                     'Tang': 'C',
                     'Al Ghafri': 'K'
                     }

temperature_ranges = {'Simion': (0, 100),
                      'Tang': (25, 25),
                      'Al Ghafri': (298.15, 473.15)
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

    return rho0, rho


def density_tang(w, T):

    w = w * 100

    rho0 = 997.1  # density of pure water (at 25°C)
    rho = rho0
    A = np.array([7.41e-3, -3.741e-5,2.252e-6, -2.06e-8])*1000
    for i, a in enumerate(A):
        rho += a * w**(i+1)

    return rho0, rho


def density_alghafri(m, T):

    a = np.zeros((4, 5))
    a[1, :] = [2863.158, -46844.356, 120760.118, -116867.722, 40285.426]
    a[2, :] = [-2000.028, 34013.518, -88557.123, 86351.784, -29910.216]
    a[3, :] = [413.046, -7125.857, 18640.780, -18244.074, 6335.275]

    b = np.zeros((2, 4))
    b[0, :] = [-1622.4, 9383.8, -14893.8, 7309.10]
    b[1, :] = [241.57, -980.97, 1482.31, -750.98]

    c = np.zeros(3)
    c[:] = [0.11725, -0.00134, 0.00056]

    rho = rho_alghafri(m, T, 1e5, a, b, c)
    rho0 = density_atm(T, 'K')

    return rho0, rho


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Simion': density_simion,
            'Tang': density_tang,
            'Al Ghafri': density_alghafri
            }

sources = [source for source in formulas]
