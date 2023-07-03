"""Gathers the formulas for the activity coefficients of KCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns one parameter
- gamma, molal activity coefficient (dimensionless)
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------

- Steiger, M., Kiekbusch, J. & Nicolai,
  An improved model incorporating Pitzer's equations for calculation of
  thermodynamic properties of pore solutions implemented into an efficient
  program code.
  Construction and Building Materials 22, 1841-1850 (2008).

NOTE: I could not find explicit info about validity domain for the KCl
      formulas in Steiger, so I kept ~ same values as for NaCl
"""

import numpy as np

from .misc import ln_gamma_extended_debye_huckel
from ..steiger import coeffs_steiger_2005, coeffs_steiger_2008
from ..pitzer import PitzerActivity

# General Info about the formulas

default_source = 'Steiger 2008'

concentration_types = {
    'Steiger 2008': 'm',
    'Tang': 'm',
}

concentration_ranges = {
    'Steiger 2008': (0, 15),  # NOT SURE (see above)
    'Tang': (1e-9, 13)
}

temperature_units = {
    'Steiger 2008': 'K',
    'Tang': 'C',
}

temperature_ranges = {
    'Steiger 2008': (278.15, 323.15),   # NOT SURE (see above)
    'Tang': (25, 25),
}


# ============================== FORMULAS ====================================


def activity_coefficient_Steiger_2008(m, T):
    coeffs = coeffs_steiger_2008.coeffs(solute='KCl', T=T)
    pitz = PitzerActivity(T=T, solute='KCl', **coeffs)
    return pitz.activity_coefficient(m=m)


def activity_coefficient_Tang(m, T):
    A = 0.5108
    B = 1.35
    C = 7.625e-3
    D = -7.892e-4
    E = 2.492e-5
    beta = -9.842e-3
    coeffs_tang_KCl = A, B, C, D, E, beta
    lng = ln_gamma_extended_debye_huckel(m, T, solute='KCl', coeffs=coeffs_tang_KCl)
    return np.exp(lng)


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {
    'Steiger 2008': activity_coefficient_Steiger_2008,
    'Tang': activity_coefficient_Tang,
}

sources = [source for source in formulas]
