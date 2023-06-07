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

from ..steiger import coeffs_steiger_2005, coeffs_steiger_2008
from ..pitzer import PitzerActivity

# General Info about the formulas

default_source = 'Steiger 2008'

concentration_types = {
    'Steiger 2008': 'm',
}

concentration_ranges = {
    'Steiger 2008': (0, 15),  # NOT SURE (see above)
}

temperature_units = {
    'Steiger 2008': 'K',
}

temperature_ranges = {
    'Steiger 2008': (278.15, 323.15),   # NOT SURE (see above)
}


# ============================== FORMULAS ====================================


def activity_coefficient_Steiger_2008(m, T):
    coeffs = coeffs_steiger_2008.coeffs(solute='KCl', T=T)
    pitz = PitzerActivity(T=T, solute='KCl', **coeffs)
    return pitz.activity_coefficient(m=m)


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {
    'Steiger 2008': activity_coefficient_Steiger_2008,
}

sources = [source for source in formulas]
