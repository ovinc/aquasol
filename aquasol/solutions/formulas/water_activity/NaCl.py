"""Gathers the formulas for the water activity of NaCl solutions.

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

- Tang, I. N., Munkelwitz, H. R. & Wang, N.
  Water activity measurements with single suspended droplets:
  The NaCl-H2O and KCl-H2O systems.
  Journal of Colloid and Interface Science 114, 409-415 (1986).
  Valid at 25°C and for solutions of molality up to ~13 mol/kg

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
"""

# TODO: add Dutcher (it has supersaturated values!)

import numpy as np

from .misc import aw_extended_debye_huckel
from ..steiger import coeffs_steiger_2005, coeffs_steiger_2008
from ..pitzer import PitzerActivity
from ....constants import charge_numbers
from ...convert import ion_quantities, ionic_strength

# General Info about the formulas

default_source = 'Clegg'

concentration_types = {
    'Clegg': 'x',
    'Tang': 'm',
    'Steiger 2005': 'm',
    'Steiger 2008': 'm',
}

concentration_ranges = {
    'Clegg': (0, 0.25),
    'Tang': (1e-9, 14),
    'Steiger 2005': (0, 13.5),
    'Steiger 2008': (0, 15),
}

temperature_units = {
    'Clegg': 'C',
    'Tang': 'C',
    'Steiger 2005': 'K',
    'Steiger 2008': 'K',
}

temperature_ranges = {
    'Clegg': (25, 25),
    'Tang': (25, 25),
    'Steiger 2005': (298.15, 298.15),
    'Steiger 2008': (278.15, 323.15),
}


# ============================== FORMULAS ====================================

def water_activity_clegg(x, T):

    x_Na, x_Cl = ion_quantities('NaCl', x=x)
    x1 = 1 - (x_Na + x_Cl)  # mole fraction of water

    z_Na, z_Cl = charge_numbers['NaCl']

    Ix = ionic_strength('NaCl', x=x)  # ionic strength

    rho = 13.0

    A_x = 2.915
    B = 24.22023
    alpha = 5.0
    W1 = 0.7945378
    U1 = 12.15304
    V1 = -12.76357

    val = 2 * A_x * Ix**(3 / 2) / (1 + rho * Ix**(1 / 2))  # 1st line
    val -= x_Na * x_Cl * B * np.exp(-alpha * Ix**(1 / 2))  # 2nd line
    val += (1 - x1) * x_Cl * (1 + z_Cl) * W1  # 5th line
    val += (1 - 2 * x1) * x_Na * x_Cl * ((1 + z_Cl)**2 / z_Cl) * U1  # 6-7th lines
    val += 4 * x1 * (2 - 3 * x1) * x_Na * x_Cl * V1  # 8th line

    f1 = np.exp(val)
    a1 = f1 * x1

    return a1


def water_activity_Tang(m, T):

    A = 0.5108
    B = 1.37
    C = 4.803e-3
    D = -2.736e-4
    E = 0
    beta = 2.796e-2

    coeffs_tang_NaCl = A, B, C, D, E, beta

    return aw_extended_debye_huckel(m, T, solute='NaCl', coeffs=coeffs_tang_NaCl)


def water_activity_Steiger_2005(m, T):
    coeffs = coeffs_steiger_2005.coeffs(solute='NaCl', T=T)
    pitz = PitzerActivity(T=T, solute='NaCl', **coeffs)
    return pitz.water_activity(m=m)


def water_activity_Steiger_2008(m, T):
    coeffs = coeffs_steiger_2008.coeffs(solute='NaCl', T=T)
    pitz = PitzerActivity(T=T, solute='NaCl', **coeffs)
    return pitz.water_activity(m=m)


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {
    'Clegg': water_activity_clegg,
    'Tang': water_activity_Tang,
    'Steiger 2005': water_activity_Steiger_2005,
    'Steiger 2008': water_activity_Steiger_2008,
}

sources = [source for source in formulas]
