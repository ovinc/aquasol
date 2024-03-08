"""Activity of solutions according to clegg

Source
------
- Clegg et al. : "Thermodynamic Properties of Aqueous Aerosols to High
Supersaturation: II" (1997). Valid at 25°C and for solutions of molality
up to ~17 mol/kg (x ~ 0.23)
"""

import numpy as np

from ....constants import charge_numbers
from ...general import SolutionFormula
from ..ionic import ion_quantities, ionic_strength


def aw_clegg(x, T, solute, coeffs):

    x_ion1, x_ion2 = ion_quantities(solute, x=x)
    x1 = 1 - (x_ion1 + x_ion2)  # mole fraction of water

    z_ion1, z_ion2 = charge_numbers[solute]

    Ix = ionic_strength(solute, x=x)  # ionic strength

    rho = 13.0

    A_x, B, alpha, W1, U1, V1 = coeffs

    val = 2 * A_x * Ix**(3 / 2) / (1 + rho * Ix**(1 / 2))  # 1st line
    val -= x_ion1 * x_ion2 * B * np.exp(-alpha * Ix**(1 / 2))  # 2nd line
    val += (1 - x1) * x_ion2 * (1 + z_ion2) * W1  # 5th line
    val += (1 - 2 * x1) * x_ion1 * x_ion2 * ((1 + z_ion2)**2 / z_ion2) * U1  # 6-7th lines
    val += 4 * x1 * (2 - 3 * x1) * x_ion1 * x_ion2 * V1  # 8th line

    f1 = np.exp(val)
    a1 = f1 * x1

    return a1


class WaterActivity_Clegg_Base(SolutionFormula):

    source ='Clegg'

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'x'

    with_water_reference = False

    def calculate(self, x, T):
        return aw_clegg(x, T, solute=self.solute, coeffs=self.coeffs.values())


class WaterActivity_Na2SO4_Clegg_Base(WaterActivity_Clegg_Base):

    solute = 'Na2SO4'
    concentration_range = (0, 0.23)

    coeffs = {
        'A_x': 2.915,
        'B': 48.56028,
        'alpha': 8.0,
        'W1': 5.555706,
        'U1': 21.88352,
        'V1': -22.81674,
    }


class WaterActivity_NaCl_Clegg_Base(WaterActivity_Clegg_Base):

    solute = 'NaCl'
    concentration_range = (0, 0.25)

    coeffs = {
        'A_x': 2.915,
        'B': 24.22023,
        'alpha': 5.0,
        'W1': 0.7945378,
        'U1': 12.15304,
        'V1': -12.76357,
    }
