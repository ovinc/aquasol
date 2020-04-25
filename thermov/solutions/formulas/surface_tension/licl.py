"""Gathers the formulas for the surface tension of LiCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns two parameters
- sigma0, sigma surface tensions in N/m of pure water and solution
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
Conde, M. R., Properties of aqueous solutions of lithium and calcium
chlorides: formulations for use in air conditioning equipment design.
International Journal of Thermal Sciences 43, 367–382 (2004).
"""


from .misc import sigma_conde, sigma_iapws


# ============================ GENERAL INFO ==================================

default_source = 'Conde'

concentration_types = {'Conde': 'w'}

concentration_ranges = {'Conde': (0, 0.45)}

temperature_units = {'Conde': 'C'}

temperature_ranges = {'Conde': (0, 100)}


# ============================== FORMULAS ====================================

def surface_tension_conde(w, T):
    """Surface tension from Conde2004. Input: weight fraction, T in K."""

    T = T + 273.15

    # Surface tension of pure water
    sigma_w = sigma_iapws(T)

    # Surface tension of the solution
    coeffs = [2.757115, -12.011299, 14.751818, 2.443204, -3.147739]
    sigma = sigma_conde(w, T, coeffs)

    return sigma_w, sigma


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {'Conde': surface_tension_conde,
            }

sources = [source for source in formulas]

