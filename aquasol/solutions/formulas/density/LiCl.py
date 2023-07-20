"""Gathers the formulas for the density of LiCl solutions.

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
- Conde, M. R., Properties of aqueous solutions of lithium and calcium
  chlorides: formulations for use in air conditioning equipment design.
  International Journal of Thermal Sciences 43, 367-382 (2004).

- Krumgalz, B. S., Pogorelsky, R. & Pitzer, K. S.
  Volumetric Properties of Single Aqueous Electrolytes from Zero to Saturation
  Concentration at 298.15 °K Represented by Pitzer's Ion-Interaction Equations.
  Journal of Physical and Chemical Reference Data 25, 663-689 (1996).
"""

from .misc import relative_rho_conde, density_pitzer
from ....water import density_atm

# General Info about the formulas

default_source = 'Conde'

concentration_types = {
    'Conde': 'r',
    'Krumgalz': 'm',
}

concentration_ranges = {
    'Conde': (0, 1.273),
    'Krumgalz': (0, 19.6),
}

temperature_units = {
    'Conde': 'K',
    'Krumgalz': 'C',
}

temperature_ranges = {
    'Conde': (273.15, 373.15),
    'Krumgalz': (25, 25),
}

# ============================== FORMULAS ====================================


def density_conde(z, T):

    coeffs = 1, 0.540966, -0.303792, 0.100791

    d = relative_rho_conde(z, coeffs)
    rho0 = density_atm(T, 'K')

    return rho0, rho0 * d


def density_krumgalz(m, T):
    return density_pitzer(m, solute='LiCl', source='Krumgalz')


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {
    'Conde': density_conde,
    'Krumgalz': density_krumgalz,
}

sources = [source for source in formulas]
