"""Duvall et al. formulas for solubility of solutions (LiBr).

Source
------
Duvall, K. N., Dirksen, J. A. & Ring, T. A.
Ostwald-Meyers Metastable Region in LiBr Crystallization—Comparison of
Measurements with Predictions.
Journal of Colloid and Interface Science 239, 391-398
(2001)

Note: the paper has sign errors that I have corrected
(see comments in coefficients below)
"""

import numpy as np

from ...general import SaturatedSolutionFormula


class Solubility_Duvall_Base(SaturatedSolutionFormula):

    source = 'Duvall'
    concentration_unit = 'x'
    temperature_unit = 'K'

    def calculate(self, T):
        """Returns mole fraction of saturated solution"""
        A, B, C = self.coeffs
        ln_x = A + B / T + C * np.log(T)
        return np.exp(ln_x)


# =============================== Steiger 2008 ===============================


class Solubility_LiBr_1H2O_Duvall_Base(Solubility_Duvall_Base):
    crystal = 'LiBr,H2O'
    temperature_range = tuple(273.15 + T for T in (34.6, 100))
    coeffs = -43.71368, 1858.62739, 6.366771  # sign error in paper last term


class Solubility_LiBr_2H2O_Duvall_Base(Solubility_Duvall_Base):
    crystal = 'LiBr,2H2O'
    temperature_range = tuple(273.15 + T for T in (5.7, 34.6))
    coeffs = -146.11879, 5671.38048, 22.078296


class Solubility_LiBr_3H2O_Duvall_Base(Solubility_Duvall_Base):
    crystal = 'LiBr,3H2O'
    temperature_range = tuple(273.15 + T for T in (-25, 5.7))  # lower bound approx
    coeffs = 377.41598, -16077.58765, -57.048733  # sign error in paper 2d term
