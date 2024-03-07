"""Gathers the formulas for the activity of KCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns one parameter
- a, water activity (dimensionless, range 0-1)
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
- Tang, I. N., Munkelwitz, H. R. & Wang, N.
  Water activity measurements with single suspended droplets:
  The NaCl-H2O and KCl-H2O systems.
  Journal of Colloid and Interface Science 114, 409-415 (1986).
  Valid at 25°C and for solutions of molality up to ~13 mol/kg

- Steiger, M., Kiekbusch, J. & Nicolai,
  An improved model incorporating Pitzer's equations for calculation of
  thermodynamic properties of pore solutions implemented into an efficient
  program code.
  Construction and Building Materials 22, 1841-1850 (2008).

NOTE: I could not find explicit info about validity domain for the KCl
      formulas in Steiger, so I kept ~ same values as for NaCl
"""

from .misc import aw_extended_debye_huckel
from ..steiger import coeffs_steiger_2008
from ..pitzer import PitzerActivity

# General Info about the formulas

default_source = 'Steiger 2008'

concentration_types = {
    'Tang': 'm',
    'Steiger 2008': 'm',
}

concentration_ranges = {
    'Tang': (1e-9, 13),
    'Steiger 2008': (0, 15),  # NOT SURE (see above)
}

temperature_units = {
    'Tang': 'C',
    'Steiger 2008': 'K',
}

temperature_ranges = {
    'Tang': (25, 25),
    'Steiger 2008': (278.15, 323.15),   # NOT SURE (see above)
}


# ============================== FORMULAS ====================================

def water_activity_Tang(m, T):

    A = 0.5108
    B = 1.35
    C = 7.625e-3
    D = -7.892e-4
    E = 2.492e-5
    beta = -9.842e-3

    coeffs_tang_KCl = A, B, C, D, E, beta

    return aw_extended_debye_huckel(m, T, solute='KCl', coeffs=coeffs_tang_KCl)


def water_activity_Steiger_2008(m, T):
    coeffs = coeffs_steiger_2008.coeffs(solute='KCl', T=T)
    pitz = PitzerActivity(T=T, solute='KCl', **coeffs)
    return pitz.water_activity(m=m)


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {
    'Tang': water_activity_Tang,
    'Steiger 2008': water_activity_Steiger_2008,
}

sources = [source for source in formulas]
