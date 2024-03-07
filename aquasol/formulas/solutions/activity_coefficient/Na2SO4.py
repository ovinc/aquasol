"""Gathers the formulas for the activity coefficients of Na2SO4 solutions.

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

Note: some potential info about validity in:
Steiger, M. & Asmussen, S.
Crystallization of sodium sulfate phases in porous materials:
The phase diagram Na2SO4-H2O and the generation of stress.
Geochimica et Cosmochimica Acta 72, 4291-4306 (2008).

For now, I have assumed validity similar to NaCl (in temperatures)
"""

from ..steiger import coeffs_steiger_2005, coeffs_steiger_2008
from ..pitzer import PitzerActivity

# General Info about the formulas

default_source = 'Steiger 2008'

concentration_types = {
    'Steiger 2005': 'm',
    'Steiger 2008': 'm',
}

concentration_ranges = {
    'Steiger 2005': (0, 12),
    'Steiger 2008': (0, 12),     # guessed identical to 2005
}

temperature_units = {
    'Steiger 2005': 'K',
    'Steiger 2008': 'K',
}

temperature_ranges = {
    'Steiger 2005': (298.15, 298.15),
    'Steiger 2008': (278.15, 323.15),
}


# ============================== FORMULAS ====================================


def activity_coefficient_Steiger_2005(m, T):
    coeffs = coeffs_steiger_2005.coeffs(solute='Na2SO4', T=T)
    pitz = PitzerActivity(T=T, solute='Na2SO4', **coeffs)
    return pitz.activity_coefficient(m=m)


def activity_coefficient_Steiger_2008(m, T):
    coeffs = coeffs_steiger_2008.coeffs(solute='Na2SO4', T=T)
    pitz = PitzerActivity(T=T, solute='Na2SO4', **coeffs)
    return pitz.activity_coefficient(m=m)


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {
    'Steiger 2005': activity_coefficient_Steiger_2005,
    'Steiger 2008': activity_coefficient_Steiger_2008,
}

sources = [source for source in formulas]
