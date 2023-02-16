"""Gathers the formulas for the density of Na2SO4 solutions.

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

- Tang, I. N. & Munkelwitz, H. R.
  Simultaneous Determination of Refractive Index and Density of an
  Evaporating Aqueous Solution Droplet.
  Aerosol Science and Technology 15, 201-207 (1991).
"""

import numpy as np

from .misc import rho_tang

# General Info about the formulas

default_source = 'Tang'

concentration_types = {'Tang': 'w',
                       }

concentration_ranges = {'Tang': (0, 0.68),
                        }

temperature_units = {'Tang': 'C',
                     }

temperature_ranges = {'Tang': (25, 25),
                      }


# ============================== FORMULAS ====================================


def density_tang(w, T):
    coeffs = np.array([8.871e-3, 3.195e-5, 2.28e-7, 0]) * 1000
    return rho_tang(w, coeffs)


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Tang': density_tang,
            }

sources = [source for source in formulas]
