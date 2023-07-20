"""Gathers the formulas for the density of Na2SO4 solutions.

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

- Tang, I. N. & Munkelwitz, H. R.
  Simultaneous Determination of Refractive Index and Density of an
  Evaporating Aqueous Solution Droplet.
  Aerosol Science and Technology 15, 201-207 (1991).

- Clegg, S. L. & Wexler, A. S.
  Densities and Apparent Molar Volumes of Atmospherically Important
  Electrolyte Solutions. 1. The Solutes H2SO4, HNO3, HCl, Na2SO4, NaNO3, NaCl,
  (NH4)2SO4, NH4NO3, and NH4Cl from 0 to 50 °C, Including Extrapolations to
  Very Low Temperature and to the Pure Liquid State, and NaHSO4, NaOH, and NH3
  at 25 °C. J. Phys. Chem. A 115, 3393-3460 (2011).
"""

import numpy as np

from ....water import density_atm
from ..clegg import density_Na2SO4_high_conc
from .misc import rho_tang

# General Info about the formulas

default_source = 'Tang'

concentration_types = {
  'Tang': 'w',
  'Clegg': 'w',
}

concentration_ranges = {
  'Tang': (0, 0.68),
  'Clegg': (0.22, 1),
}

temperature_units = {
  'Tang': 'C',
  'Clegg': 'K',
}

temperature_ranges = {
  'Tang': (25, 25),
  'Clegg': (273.15, 348.15),  # 0°C to 75°C
}


# ============================== FORMULAS ====================================


def density_tang(w, T):
    coeffs = np.array([8.871e-3, 3.195e-5, 2.28e-7, 0]) * 1000
    return rho_tang(w, coeffs)


def density_clegg(w, T):
    rho_w = density_atm(T=T, unit='K')
    # NOTE : there is also a formula that I coded for low concentration
    # but there seems to be a problem somewhere because it's not continuous
    # with the high concentration formula
    # (see clegg.py module)
    return rho_w, density_Na2SO4_high_conc(w, T)


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {
    'Tang': density_tang,
    'Clegg': density_clegg
}

sources = [source for source in formulas]
