"""Various functions for calculation of the water activity of solutions."""


import numpy as np

from ....constants import charge_numbers
from ...convert import ionic_strength


def ln_gamma_extended_debye_huckel(m, T, solute, coeffs):
    """Mix of Hamer & Wu 1972 and Tang, Munkelwitz and Wang 1986.

    Used for NaCl and KCl
    """
    z1, z2 = charge_numbers[solute]
    A, B, C, D, E, beta = coeffs
    I = ionic_strength(solute, m=m)  # ionic strength

    ln_gamma = - z1 * z2 * A * np.sqrt(I) / (1 + B * np.sqrt(I))
    ln_gamma += (beta * I) + (C * I**2) + (D * I**3) + (E * I**4)

    return ln_gamma
