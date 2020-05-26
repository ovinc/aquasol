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
"""


from .misc import aw_clegg

# General Info about the formulas

default_source = 'Clegg'

concentration_types = {'Clegg': 'x'}

concentration_ranges = {'Clegg': (0, 0.23)}

temperature_units = {'Clegg': 'C'}

temperature_ranges = {'Clegg': (25, 25)}


# ============================== FORMULAS ====================================

def water_activity_clegg(x, T):
 
    coeffs = 2.915, 48.56028, 8.0, 5.555706, 21.88352, -22.81674

    a1 = aw_clegg(x, T, 'Na2SO4', coeffs)

    return a1

# ========================== WRAP-UP OF FORMULAS =============================

formulas = {'Clegg': water_activity_clegg}

sources = [source for source in formulas]
