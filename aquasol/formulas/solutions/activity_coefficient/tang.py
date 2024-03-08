"""Activity coefficients of solutions according to Tang

NOTE: Very similar in structure to water_activity.tang

Source
------
- Tang, I. N., Munkelwitz, H. R. & Wang, N.
  Water activity measurements with single suspended droplets:
  The NaCl-H2O and KCl-H2O systems.
  Journal of Colloid and Interface Science 114, 409-415 (1986).
  Valid at 25°C and for solutions of molality up to ~13 mol/kg
"""

import numpy as np

from ....constants import charge_numbers
from ...general import SolutionFormula
from ..ionic import ionic_strength


def ln_gamma_extended_debye_huckel(m, T, solute, coeffs):
    """Mix of Hamer & Wu 1972 and Tang, Munkelwitz and Wang 1986.

    Used for NaCl and KCl
    """
    z1, z2 = charge_numbers[solute]
    A, B, C, D, E, beta = coeffs
    I = ionic_strength(solute, m=m)

    ln_gamma = - z1 * z2 * A * np.sqrt(I) / (1 + B * np.sqrt(I))
    ln_gamma += (beta * I) + (C * I**2) + (D * I**3) + (E * I**4)

    return ln_gamma


class ActivityCoefficient_Tang_Base(SolutionFormula):

    source ='Tang'

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'm'

    with_water_reference = False

    def calculate(self, m, T):
        log_g = ln_gamma_extended_debye_huckel(
            m=m,
            T=T,
            solute=self.solute,
            coeffs=self.coeffs.values(),
        )
        return 10**(log_g)


class ActivityCoefficient_NaCl_Tang_Base(ActivityCoefficient_Tang_Base):

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


class ActivityCoefficient_KCl_Tang_Base(ActivityCoefficient_Tang_Base):

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
