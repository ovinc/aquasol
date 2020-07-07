"""Gathers the formulas for the density of LiCl solutions.

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
- Conde, M. R., Properties of aqueous solutions of lithium and calcium
chlorides: formulations for use in air conditioning equipment design.
International Journal of Thermal Sciences 43, 367–382 (2004).
"""

from .misc import relative_rho_conde
from ....water import density_atm

# General Info about the formulas

default_source = 'Conde'

concentration_types = {'Conde': 'mass_ratio'
                       }

concentration_ranges = {'Conde': (0, 1.273)
                        }

temperature_units = {'Conde': 'K'
                     }

temperature_ranges = {'Conde': (273.15, 373.15)
                      }

# ============================== FORMULAS ====================================


def density_conde(z, T):

    coeffs = 1, 0.540966, -0.303792, 0.100791

    d = relative_rho_conde(z, coeffs)
    rho0 = density_atm(T, 'K')

    return rho0, rho0 * d


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Conde': density_conde
            }

sources = [source for source in formulas]
