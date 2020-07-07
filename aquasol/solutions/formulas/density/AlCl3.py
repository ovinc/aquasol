"""Gathers the formulas for the density of AlCl3 solutions.

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
"""

import numpy as np

from .misc import rho_alghafri
from ....water import density_atm

# General Info about the formulas

default_source = 'Al Ghafri'

concentration_types = {'Al Ghafri': 'm'
                       }

concentration_ranges = {'Al Ghafri': (0, 2)
                        }

temperature_units = {'Al Ghafri': 'K'
                     }

temperature_ranges = {'Al Ghafri': (298.15, 473.15)
                      }


# ============================== FORMULAS ====================================


def density_alghafri(m, T):

    a = np.zeros((4, 5))
    a[1, :] = [1326.366, -310263.216, 443804.244, 0, 0]
    a[2, :] = [-1804.785, 527875.006, -755878.487, 0, 0]
    a[3, :] = [727.779, -218520.857, 312961.409, 0, 0]

    b = np.zeros((2, 4))
    b[0, :] = [-1622.4, 9383.8, -14893.8, 7309.10]
    b[1, :] = [0, 0, 0, 0]

    c = np.zeros(3)
    c[:] = [0.11725, -0.04236, 0.01319]

    rho = rho_alghafri(m, T, 1e5, a, b, c)
    rho0 = density_atm(T, 'K')

    return rho0, rho


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Al Ghafri': density_alghafri
            }

sources = [source for source in formulas]
