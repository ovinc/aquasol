"""Gathers the formulas for the surface tension of CaCl2 solutions.

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

- Dutcher: Dutcher, C. S., Wexler, A. S. & Clegg, S. L. Surface Tensions of
Inorganic Multicomponent Aqueous Electrolyte Solutions and Melts.
J. Phys. Chem. A 114, 12216–12230 (2010).
"""


from .misc import sigma_conde, sigma_dutcher, sigma_iapws


# ============================ GENERAL INFO ==================================

sources = ['Conde', 'Dutcher']
default_source = 'Dutcher'

concentration_types = {'Conde': 'w',
                       'Dutcher': 'x'}

concentration_ranges = {'Conde': (0, 0.45),
                        'Dutcher': (0, 0.117)}

temperature_units = {'Conde': 'C',
                     'Dutcher': 'K'}

temperature_ranges = {'Conde': (0, 100),
                      'Dutcher': (243.15, 373.15)}


# ============================== FORMULAS ====================================

def surface_tension_conde(w, T):
    """Surface tension from Conde2004. Input: weight fraction, T in K."""

    T = T + 273.15

    # Surface tension of pure water
    sigma_w = sigma_iapws(T)

    # Surface tension of the solution
    coeffs = [2.33067, -10.78779, 13.56611, 1.95017, -1.77990]
    sigma = sigma_conde(w, T, coeffs)

    return sigma_w, sigma


def surface_tension_dutcher(x, T):
    """Surface tension calculated from Dutcher 2010.
    Input: mole fraction x, temperature T in K."""

    # Coefficients (Table 3)
    c1 = 195.67     # note - other values possible: (189, -0.03952)
    c2 = -0.04541
    # Coefficients (Table 5)
    aws = -19.766
    bws = 0.575
    asw = 0
    bsw = 0

    coeffs_table3 = c1, c2
    coeffs_table5 = aws, bws, asw, bsw

    sigma_w = sigma_iapws(T)
    sigma = sigma_dutcher(x, T, coeffs_table3, coeffs_table5)

    return sigma_w, sigma


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {'Conde': surface_tension_conde,
            'Dutcher': surface_tension_dutcher,
            }

