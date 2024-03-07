"""Gathers the formulas for the activity of CaCl2 solutions.

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
- Conde, M. R., Properties of aqueous solutions of lithium and calcium
chlorides: formulations for use in air conditioning equipment design.
International Journal of Thermal Sciences 43, 367-382 (2004).
"""

# TODO: add Dutcher (it has supersaturated values!)


from .misc import aw_conde

# General Info about the formulas

default_source = 'Conde'

concentration_types = {'Conde': 'w'}

# Approximative, actually depends on temperature. Conde not defined in w=0 ...
concentration_ranges = {'Conde': (0.0001, 0.6)}

temperature_units = {'Conde': 'C'}

temperature_ranges = {'Conde': (0, 100)}   # Deduced from data presented in Fig. 3


# ============================== FORMULAS ====================================

def water_activity_conde(w, T):
    """Water activity for LiCl as a function of concentration according to Conde."""

    T = T + 273.15
    coeffs = 0.31, 3.698, 0.6, 0.231, 4.584, 0.49, 0.478, -5.20, -0.4, 0.018
    aw = aw_conde(w, T, coeffs)
    return aw


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {'Conde': water_activity_conde}

sources = [source for source in formulas]
