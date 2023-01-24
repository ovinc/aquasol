"""Gathers the formulas for the activity of NaCl solutions.

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
  Journal of Colloid and Interface Science 114, 409–415 (1986).
  Valid at 25°C and for solutions of molality up to ~13 mol/kg
"""

from .misc import aw_extended_debye_huckel

# General Info about the formulas

default_source = 'Tang'

concentration_types = {'Tang': 'm'}

concentration_ranges = {'Tang': (0, 13)}

temperature_units = {'Tang': 'C'}

temperature_ranges = {'Tang': (25, 25)}


# ============================== FORMULAS ====================================

A = 0.5108
B = 1.35
C = 7.625e-3
D = -7.892e-4
E = 2.492e-5
beta = -9.842e-3

coeffs_tang_KCl = A, B, C, D, E, beta

def water_activity_Tang(m, T):
    return aw_extended_debye_huckel(m, T, solute='KCl', coeffs=coeffs_tang_KCl)


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {'Tang': water_activity_Tang}

sources = [source for source in formulas]