"""Gathers the formulas for the density of CaCl2 solutions.

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
- Al Ghafri et al., Densities of Aqueous MgCl2(aq), CaCl2 (aq), KI(aq),
NaCl(aq), KCl(aq), AlCl3(aq), and (0.964 NaCl + 0.136 KCl)(aq) at
Temperatures Between (283 and 472) K, Pressures up to 68.5 MPa, and
Molalities up to 6 mol·kg −1.
Journal of Chemical & Engineering Data 57, 1288-1304 (2012).

- Conde, M. R., Properties of aqueous solutions of lithium and calcium
chlorides: formulations for use in air conditioning equipment design.
International Journal of Thermal Sciences 43, 367–382 (2004).
"""

import numpy as np

from .misc import rho_alghafri, relative_rho_conde
from thermov.water import density_atm

# General Info about the formulas

default_source = 'Conde'

concentration_types = {'Al Ghafri': 'm',
                       'Conde': 'mass_ratio'
                       }

concentration_ranges = {'Al Ghafri': (0, 6),
                        'Conde': (0, 1.5)
                        }

temperature_units = {'Al Ghafri': 'K',
                     'Conde': 'K'
                     }

temperature_ranges = {'Al Ghafri': (298.15, 473.15),
                      'Conde': (273.15, 373.15)
                      }


# ============================== FORMULAS ====================================


def density_alghafri(m, T):

    a = np.zeros((4, 5))
    a[1, :] = [2546.760, -39884.946, 102056.957, -98403.334, 33976.048]
    a[2, :] = [-1362.157, 22785.572, -59216.108, 57894.824, -20222.898]
    a[3, :] = [217.778, -3770.645, 9908.135, -9793.484, 3455.587]

    b = np.zeros((2, 4))
    b[0, :] = [-1622.4, 9383.8, -14893.8, 7309.10]
    b[1, :] = [307.24, -1259.10, 2034.03, -1084.94]

    c = np.zeros(3)
    c[:] = [0.11725, -0.00493, 0.00231]

    rho = rho_alghafri(m, T, 1e5, a, b, c)
    rho0 = density_atm(T, 'K')

    return rho0, rho


def density_conde(z, T):

    coeffs = 1, 0.836014, -0.436300, 0.105642

    d = relative_rho_conde(z, coeffs)
    rho0 = density_atm(T, 'K')

    return rho0, rho0 * d


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Al Ghafri': density_alghafri,
            'Conde': density_conde
            }

sources = [source for source in formulas]
