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
- Clegg et al. : "Thermodynamic Properties of Aqueous Aerosols to High
Supersaturation: II" (1997). Valid at 25°C and for solutions of molality
up to ~17 mol/kg (x ~ 0.23)
"""

import numpy as np

from ....constants import charge_numbers
from ...convert import ion_quantities, ionic_strength

# General Info about the formulas

default_source = 'Clegg'

concentration_types = {'Clegg': 'x'}

concentration_ranges = {'Clegg': (0, 0.23)}

temperature_units = {'Clegg': 'C'}

temperature_ranges = {'Clegg': (25, 25)}


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


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {'Clegg': water_activity_clegg}

sources = [source for source in formulas]