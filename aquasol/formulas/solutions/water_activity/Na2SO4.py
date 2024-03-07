"""Gathers the formulas for the activity of Na2SO4 solutions.

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
- Clegg et al. : "Thermodynamic Properties of Aqueous Aerosols to High
Supersaturation: II" (1997). Valid at 25°C and for solutions of molality
up to ~17 mol/kg (x ~ 0.23)

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

For now, I have assumed validity similar to NaCl (in temperatures)
"""

from .misc import aw_clegg
from ..steiger import coeffs_steiger_2005, coeffs_steiger_2008
from ..pitzer import PitzerActivity

# General Info about the formulas

default_source = 'Steiger 2008'

concentration_types = {
    'Clegg': 'x',
    'Steiger 2005': 'm',
    'Steiger 2008': 'm',
}

concentration_ranges = {
    'Clegg': (0, 0.23),
    'Steiger 2005': (0, 12),
    'Steiger 2008': (0, 12),
}

temperature_units = {
    'Clegg': 'C',
    'Steiger 2005': 'K',
    'Steiger 2008': 'K',
}

temperature_ranges = {
    'Clegg': (25, 25),
    'Steiger 2005': (298.15, 298.15),
    'Steiger 2008': (278.15, 323.15),
}


# ============================== FORMULAS ====================================

def water_activity_clegg(x, T):
    coeffs = 2.915, 48.56028, 8.0, 5.555706, 21.88352, -22.81674
    a1 = aw_clegg(x, T, 'Na2SO4', coeffs)
    return a1


def water_activity_Steiger_2005(m, T):
    coeffs = coeffs_steiger_2005.coeffs(solute='Na2SO4', T=T)
    pitz = PitzerActivity(T=T, solute='Na2SO4', **coeffs)
    return pitz.water_activity(m=m)


def water_activity_Steiger_2008(m, T):
    coeffs = coeffs_steiger_2008.coeffs(solute='Na2SO4', T=T)
    pitz = PitzerActivity(T=T, solute='Na2SO4', **coeffs)
    return pitz.water_activity(m=m)


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {
    'Clegg': water_activity_clegg,
    'Steiger 2005': water_activity_Steiger_2005,
    'Steiger 2008': water_activity_Steiger_2008,
}

sources = [source for source in formulas]
