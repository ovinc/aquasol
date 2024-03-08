"""Various functions for calculation of the water activity of solutions."""


import numpy as np

from ....constants import Mw, charge_numbers, dissociation_numbers




def aw_extended_debye_huckel(m, T, solute, coeffs):
    """Mix of Hamer & Wu 1972 and Tang, Munkelwitz and Wang 1986.

    Used for NaCl and KCl
    """
    z1, z2 = charge_numbers[solute]
    nu = sum(dissociation_numbers[solute])

    A, B, C, D, E, beta = coeffs

    b = 1 + B * np.sqrt(m)

    term1 = (z1 * z2 * A / (B**3 * m)) * (b - 4.60517 * np.log10(b) - 1 / b)
    term2 = - (beta * m / 2) - (2 / 3 * C * m**2) - (3 / 4 * D * m**3) - (4 / 5 * E * m**4)

    phi =  1 - 2.302585 * (term1 + term2)  # osmotic coefficient

    return np.exp(-nu * Mw * phi * m)