"""Activity of solutions according to Tang

NOTE: Very similar in structure to activity_coefficient.tang

Source
------
- Tang, I. N., Munkelwitz, H. R. & Wang, N.
  Water activity measurements with single suspended droplets:
  The NaCl-H2O and KCl-H2O systems.
  Journal of Colloid and Interface Science 114, 409-415 (1986).
  Valid at 25°C and for solutions of molality up to ~13 mol/kg
"""

import numpy as np

from ....constants import Mw, get_solute
from ...general import SolutionFormula


def aw_extended_debye_huckel(m, solute, coeffs):
    """Mix of Hamer & Wu 1972 and Tang, Munkelwitz and Wang 1986.

    Used for NaCl and KCl at 25°C
    """
    salt = get_solute(formula=solute)
    z1, z2 = tuple(abs(z) for z in salt.charges)
    nu = sum(salt.stoichiometry)

    A, B, C, D, E, beta = coeffs

    b = 1 + B * np.sqrt(m)

    term1 = (z1 * z2 * A / (B**3 * m)) * (b - 4.60517 * np.log10(b) - 1 / b)
    term2 = - (beta * m / 2) - (2 / 3 * C * m**2) - (3 / 4 * D * m**3) - (4 / 5 * E * m**4)

    phi =  1 - 2.302585 * (term1 + term2)  # osmotic coefficient

    return np.exp(-nu * Mw * phi * m)


class WaterActivity_Tang_Base(SolutionFormula):

    source ='Tang'

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'm'

    with_water_reference = False

    def calculate(self, m, T):
        return aw_extended_debye_huckel(
            m=m,
            solute=self.solute,
            coeffs=self.coeffs.values(),
        )


class WaterActivity_NaCl_Tang_Base(WaterActivity_Tang_Base):

    solute = 'NaCl'
    concentration_range = (1e-9, 14)

    coeffs = {
        'A': 0.5108,
        'B': 1.37,
        'C': 4.803e-3,
        'D': -2.736e-4,
        'E': 0,
        'beta': 2.796e-2,
    }


class WaterActivity_KCl_Tang_Base(WaterActivity_Tang_Base):

    solute = 'KCl'
    concentration_range = (1e-9, 13)

    coeffs = {
        'A': 0.5108,
        'B': 1.35,
        'C': 7.625e-3,
        'D': -7.892e-4,
        'E': 2.492e-5,
        'beta': -9.842e-3,
    }

