"""Gathers the formulas for the surface tension of NaCl solutions.

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
- Dutcher: Dutcher, C. S., Wexler, A. S. & Clegg, S. L.
  Surface Tensions of Inorganic Multicomponent Aqueous Electrolyte Solutions and Melts.
  J. Phys. Chem. A 114, 12216-12230 (2010).

- Talreja-Muthreja, T., Linnow, K., Enke, D. & Steiger
  M. Deliquescence of NaCl Confined in Nanoporous Silica.
  Langmuir 38, 10963-10974 (2022).
"""


# TODO: add data from Ali 2006


from .misc import sigma_dutcher, sigma_iapws


# ============================ GENERAL INFO ==================================

default_source = 'Dutcher'

concentration_types = {'Dutcher': 'x',
                       'Steiger': 'm',
                       }

concentration_ranges = {'Dutcher': (0, 0.145),
                        'Steiger': (0, 7),     # approx (up to saturation)
                        }

temperature_units = {'Dutcher': 'K',
                     'Steiger': 'C',
                     }

temperature_ranges = {'Dutcher': (263.13, 473.15),
                      'Steiger': (-10, 50)
                      }


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


def surface_tension_steiger(m, T):
    """Surface tension calculated from Talreja-Muthreja et al. 2022
    Input: molality m, temperature T in Celsius."""
    sigma_w = sigma_iapws(T + 273.15)
    sigma = sigma_w + 0.00166 * m
    return sigma_w, sigma


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {'Dutcher': surface_tension_dutcher,
            'Steiger': surface_tension_steiger
            }

sources = [source for source in formulas]
