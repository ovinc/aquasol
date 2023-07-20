"""Gathers the formulas for the density of MgCl2 solutions.

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
- Al Ghafri et al., Densities of Aqueous MgCl2(aq), CaCl2 (aq), KI(aq),
  NaCl(aq), KCl(aq), AlCl3(aq), and (0.964 NaCl + 0.136 KCl)(aq) at
  Temperatures Between (283 and 472) K, Pressures up to 68.5 MPa, and
  Molalities up to 6 mol·kg -1.
  Journal of Chemical & Engineering Data 57, 1288-1304 (2012).

- Krumgalz, B. S., Pogorelsky, R. & Pitzer, K. S.
  Volumetric Properties of Single Aqueous Electrolytes from Zero to Saturation
  Concentration at 298.15 °K Represented by Pitzer's Ion-Interaction Equations.
  Journal of Physical and Chemical Reference Data 25, 663-689 (1996).

"""

import numpy as np

from .misc import rho_alghafri, density_pitzer

# General Info about the formulas

default_source = 'Al Ghafri'

concentration_types = {
    'Al Ghafri': 'm',
    'Krumgalz': 'm',
}

concentration_ranges = {
    'Al Ghafri': (0, 5),
    'Krumgalz': (0, 5.8),
}

temperature_units = {
    'Al Ghafri': 'K',
    'Krumgalz': 'C',
}

temperature_ranges = {
    'Al Ghafri': (298.15, 473.15),
    'Krumgalz': (25, 25),
}

# ============================== FORMULAS ====================================


def density_alghafri(m, T):

    a = np.zeros((4, 5))
    a[1, :] = [2385.823, -38428.112, 99526.269, -97041.399, 33841.139]
    a[2, :] = [-1254.938, 21606.295, -56988.274, 56465.943, -19934.064]
    a[3, :] = [192.534, -3480.374, 9345.908, -9408.904, 3364.018]

    b = np.zeros((2, 4))
    b[0, :] = [-1622.4, 9383.8, -14893.8, 7309.10]
    b[1, :] = [358.00, -1597.10, 2609.47, -1383.91]

    c = np.zeros(3)
    c[:] = [0.11725, -0.00789, 0.00142]

    rho = rho_alghafri(m, T, 1e5, a, b, c)
    rho0 = rho_alghafri(0, T, 1e5, a, b, c)

    return rho0, rho


def density_krumgalz(m, T):
    return density_pitzer(m, solute='MgCl2', source='Krumgalz')


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {
    'Al Ghafri': density_alghafri,
    'Krumgalz': density_krumgalz,
}

sources = [source for source in formulas]
