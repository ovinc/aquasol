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
- Dutcher: Dutcher, C. S., Wexler, A. S. & Clegg, S. L. Surface Tensions of
Inorganic Multicomponent Aqueous Electrolyte Solutions and Melts.
J. Phys. Chem. A 114, 12216–12230 (2010).
"""


# TODO: add data from Ali 2006


from .surface_tension_misc import sigma_dutcher, sigma_iapws


# ============================ GENERAL INFO ==================================

sources = ['Dutcher']
default_source = 'Dutcher'

concentration_types = {'Dutcher': 'x'}

concentration_ranges = {'Dutcher': (0, 0.145)}

temperature_units = {'Dutcher': 'K'}

temperature_ranges = {'Dutcher': (263.13, 473.15)}


# ============================== FORMULAS ====================================

def surface_tension_dutcher(x, T):
    """Surface tension calculated from Dutcher 2010.
    Input: mole fraction x, temperature T in K."""

    # Coefficients (Table 3)
    c1 = 191.16     # note - other values possible: (193.48, -0.07188)
    c2 = -0.0747
    # Coefficients (Table 5)
    aws = 232.54
    bws = -0.245
    asw = -142.42
    bsw = 0

    coeffs_table3 = c1, c2
    coeffs_table5 = aws, bws, asw, bsw

    sigma_w = sigma_iapws(T)
    sigma = sigma_dutcher(x, T, coeffs_table3, coeffs_table5)

    return sigma_w, sigma


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {'Dutcher': surface_tension_dutcher,
            }

