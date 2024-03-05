"""Gathers the formulas for the activity coefficients of NaCl solutions.

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

- Steiger, M.,
  Crystal growth in porous materials—I:
  The crystallization pressure of large crystals.
  Journal of Crystal Growth 282, 455-469 (2005).
  Valid at 25°C and up to 13.5 mol/kg

- Steiger, M., Kiekbusch, J. & Nicolai,
  An improved model incorporating Pitzer's equations for calculation of
  thermodynamic properties of pore solutions implemented into an efficient
  program code.
  Construction and Building Materials 22, 1841-1850 (2008).

(some info of domain of validity of expressions in the following paper:)
Dorn, J. & Steiger, M. Measurement and Calculation of Solubilities in the
Ternary System NaCH 3 COO + NaCl + H 2 O from 278 K to 323 K.
J. Chem. Eng. Data 52, 1784-1790 (2007).)

- Tang, I. N., Munkelwitz, H. R. & Wang, N.
  Water activity measurements with single suspended droplets:
  The NaCl-H2O and KCl-H2O systems.
  Journal of Colloid and Interface Science 114, 409-415 (1986).
  Valid at 25°C and for solutions of molality up to ~13 mol/kg
"""

import numpy as np

from .misc import ln_gamma_extended_debye_huckel
from ..steiger import coeffs_steiger_2005, coeffs_steiger_2008
from ..pitzer import PitzerActivity

# General Info about the formulas

default_source = 'Steiger 2008'

concentration_types = {
    'Steiger 2005': 'm',
    'Steiger 2008': 'm',
    'Tang': 'm',
}

concentration_ranges = {
    'Steiger 2005': (0, 13.5),
    'Steiger 2008': (0, 15),
    'Tang': (0, 14),
}

temperature_units = {
    'Steiger 2005': 'K',
    'Steiger 2008': 'K',
    'Tang': 'C',
}

temperature_ranges = {
    'Steiger 2005': (298.15, 298.15),
    'Steiger 2008': (273.15, 323.15),
    'Tang': (25, 25),
}


# ============================== FORMULAS ====================================


def activity_coefficient_Steiger_2005(m, T):
    coeffs = coeffs_steiger_2005.coeffs(solute='NaCl', T=T)
    pitz = PitzerActivity(T=T, solute='NaCl', **coeffs)
    return pitz.activity_coefficient(m=m)


def activity_coefficient_Steiger_2008(m, T):
    coeffs = coeffs_steiger_2008.coeffs(solute='NaCl', T=T)
    pitz = PitzerActivity(T=T, solute='NaCl', **coeffs)
    return pitz.activity_coefficient(m=m)


def activity_coefficient_Tang(m, T):
    A = 0.5108
    B = 1.37
    C = 4.803e-3
    D = -2.736e-4
    E = 0
    beta = 2.796e-2
    coeffs_tang_NaCl = A, B, C, D, E, beta
    log_g = ln_gamma_extended_debye_huckel(m, T, solute='NaCl', coeffs=coeffs_tang_NaCl)
    return 10**(log_g)


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {
    'Steiger 2005': activity_coefficient_Steiger_2005,
    'Steiger 2008': activity_coefficient_Steiger_2008,
    'Tang': activity_coefficient_Tang,
}

sources = [source for source in formulas]
