"""Activity of solutions according to Pitzer original paper.

NOTE: Almost identical in structure to activity_coefficient.pitzer

Sources
-------
Patil, K. R., Tripathi, A. D., Pathak, G. & Katti, S. S.
Thermodynamic Properties of Aqueous Electrolyte Solutions.
1. Vapor Pressure of Aqueous Solutions of LiCI, LiBr, and LiI.
J. Chem. Eng. Data 35, 166-168
(1990)
"""

# TODO: Patil has a correction for second virial coefficient of water that I
# have not included here (B_T)

# TODO: Add coefficients for LiI

import numpy as np

from ...water.vapor_pressure import VaporPressure_IAPWS
from ...general import SolutionFormula


class WaterActivity_Patil_Base(SolutionFormula):

    source = 'Patil'

    temperature_unit = 'K'
    temperature_range = (298.15, 348.15) # Extended 5°C from their meas. range

    concentration_unit = 'm'

    with_water_reference = False

    def _coeff(self, m, coeffs):
        """Common calculations for coeffs A, B, C as a function of m"""
        X0, X1, X2, X3 = coeffs
        return X0 + X1 * m + X2 * m**2 + X3 * m**3

    def calculate(self, m, T):
        A = self._coeff(m, coeffs=self.coeffs['A'])
        B = self._coeff(m, coeffs=self.coeffs['B'])
        C = self._coeff(m, coeffs=self.coeffs['C'])
        log_p_kPa = A + B / T + C / T**2
        p = 1e3 * 10**log_p_kPa
        vapor_pressure = VaporPressure_IAPWS()
        psat = vapor_pressure.calculate(T=T)
        return p / psat


# ============================ Different solutes =============================


class WaterActivity_LiCl_Patil_Base(WaterActivity_Patil_Base):
    solute = 'LiCl'
    concentration_range = (3, 18.5)
    coeffs = {
        'A': (7.323_3550, -0.062_3661, 0.006_1613, -0.000_1042),
        'B': (-1718.1570, 8.2255, -2.2131, 0.0246),
        'C': (-97_575.680, 3839.979, -421.429, 16.731),
    }


class WaterActivity_LiBr_Patil_Base(WaterActivity_Patil_Base):
    solute = 'LiBr'
    concentration_range = (2, 16)
    coeffs = {
        'A': (8.064_8240, -0.103_6791, -0.012_3511, 0.000_9890),
        'B': (-2235.3810, 62.4534, 5.2484, -0.5253),
        'C': (-6478.216, -10_555.860, -724.251, 66.490),
    }
