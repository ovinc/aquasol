"""Gathers the formulas for the electrical conductivity of NaCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns one parameter
- sigma, electrical conductivity, in S/m
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
- Sinmyo, R. & Keppler
  H. Electrical conductivity of NaCl-bearing aqueous fluids to 600 °C and 1 GPa.
  Contrib Mineral Petrol 172, 4 (2017).
"""

import numpy as np
from aquasol.water import density_atm

# ----------------------------------------------------------------------------

default_source = 'Sinmyo'

concentration_types = {'Sinmyo': 'w'}

concentration_ranges = {'Sinmyo': (0, 0.06)}  # approx. 1M NaCl

temperature_units = {'Sinmyo': 'K'}

temperature_ranges = {'Sinmyo': (100 + 273.15, 600 + 273.15)}


# ============================== FORMULAS ====================================


# FOR NOW THIS DOES NOT WORK WELL


def lambda_0(T, rho):
    """Molar conductivity of NaCl in water at infinite dilution (S cm^2 mol^-1).

    Used in Sinmyo's equation for NaCl solution conductivity.
    """
    return 1573 - 1212 * rho + 537_062 / T - 208_122_721 / T**2

def conductivity_NaCl_Sinmyo(w, T):
    """w weight fraction, T temperature in K"""
    rho = density_atm(T=T, unit='K') / 1000  # pure water density in g / cm^3
    log_sigma = -1.7060 - 93.78 / T + 0.8075 * np.log(w) + 3.0781 * np.log(rho) + np.log(lambda_0(T, rho))
    return np.exp(log_sigma)

# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Sinmyo': conductivity_NaCl_Sinmyo}

sources = [source for source in formulas]
