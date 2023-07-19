"""Gathers the formulas for the density of NaCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns two parameters:
- rho0, density of pure water in kg / m^3
- rho, density of solution in kg / m^3
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------

- Simion (default) : "Mathematical modelling of density and
  viscosity of NaCl aqueous solutions" (2015). Valid from w = 0 to w = 0.26
  and for temperatures between 0 and 100°C

- Tang: "Chemical and size effects of hygroscopic aerosols on light
  scattering coefficients" (1996). Valid at 25°C and from w = 0 to w ~= 0.5

- Al Ghafri et al., Densities of Aqueous MgCl 2 (aq), CaCl 2 (aq), KI(aq),
  NaCl(aq), KCl(aq), AlCl 3 (aq), and (0.964 NaCl + 0.136 KCl)(aq) at
  Temperatures Between (283 and 472) K, Pressures up to 68.5 MPa, and
  Molalities up to 6 mol·kg -1.
  Journal of Chemical & Engineering Data 57, 1288-1304 (2012).

- Steiger:
  Talreja-Muthreja, T., Linnow, K., Enke, D. & Steiger, M.
  Deliquescence of NaCl Confined in Nanoporous Silica.
  Langmuir 38, 10963-10974 (2022).

- Krumgalz, B. S., Pogorelsky, R. & Pitzer, K. S.
  Volumetric Properties of Single Aqueous Electrolytes from Zero to Saturation
  Concentration at 298.15 °K Represented by Pitzer's Ion-Interaction Equations.
  Journal of Physical and Chemical Reference Data 25, 663-689 (1996).
"""

import numpy as np

from .misc import rho_alghafri, rho_tang, density_pitzer

# General Info about the formulas

default_source = 'Simion'

concentration_types = {'Simion': 'w',
                       'Tang': 'w',
                       'Al Ghafri': 'm',
                       'Steiger': 'm',
                       'Krumgalz': 'm',
                       }

concentration_ranges = {'Simion': (0, 0.26),
                        'Tang': (0, 0.5),
                        'Al Ghafri': (0, 6),
                        'Steiger': (0, 14),
                        'Krumgalz': (0, 6.2),
                        }

temperature_units = {'Simion': 'C',
                     'Tang': 'C',
                     'Al Ghafri': 'K',
                     'Steiger': 'C',
                     'Krumgalz': 'C',
                     }

temperature_ranges = {'Simion': (0, 100),
                      'Tang': (25, 25),
                      'Al Ghafri': (298.15, 473.15),
                      'Steiger': (25, 25),
                      'Krumgalz': (25, 25),
                      }


# ============================== FORMULAS ====================================


def density_simion(w, T):

    w = w * 100  # avoid using *= to not mutate objects in place
    T = T + 273.15  # same

    a1 = 750.2834; a2 = 26.7822; a3 = -0.26389
    a4 = 1.90165; a5 = -0.11734; a6 = 0.00175
    a7 = -0.003604; a8 = 0.0001701; a9 = -0.00000261

    rho0 = a1 + a4*T + a7*T**2  # density of pure water
    rho = rho0 + a2*w + a3*w**2 + (a5*w + a6*w**2) * T + (a8*w + a9*w**2) * T**2

    return rho0, rho


def density_tang(w, T):
    coeffs = np.array([7.41e-3, -3.741e-5, 2.252e-6, -2.06e-8]) * 1000
    return rho_tang(w, coeffs)


def density_alghafri(m, T):

    a = np.zeros((4, 5))
    a[1, :] = [2863.158, -46844.356, 120760.118, -116867.722, 40285.426]
    a[2, :] = [-2000.028, 34013.518, -88557.123, 86351.784, -29910.216]
    a[3, :] = [413.046, -7125.857, 18640.780, -18244.074, 6335.275]

    b = np.zeros((2, 4))
    b[0, :] = [-1622.4, 9383.8, -14893.8, 7309.10]
    b[1, :] = [241.57, -980.97, 1482.31, -750.98]

    c = np.zeros(3)
    c[:] = [0.11725, -0.00134, 0.00056]

    rho = rho_alghafri(m, T, 1e5, a, b, c)
    rho0 = rho_alghafri(0, T, 1e5, a, b, c)

    return rho0, rho


def density_steiger(m, T):
    return density_pitzer(m, solute='NaCl', source='Steiger')


def density_krumgalz(m, T):
    return density_pitzer(m, solute='NaCl', source='Krumgalz')


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Simion': density_simion,
            'Tang': density_tang,
            'Al Ghafri': density_alghafri,
            'Steiger': density_steiger,
            'Krumgalz': density_krumgalz,
            }

sources = [source for source in formulas]
