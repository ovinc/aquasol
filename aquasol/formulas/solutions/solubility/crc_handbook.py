"""Solubility of salts from the CRC Handbook.

Based on polynomial fits of the CRC Handbook data

Sources
-------
- CRC Handbook of Chemistry and Physics, 104th Edition
  Section: 4 | Solubility of Common Inorganic Salts as a Function of Temperature
  https://hbcp.chemnetbase.com/documents/04_29/04_29_0001.xhtml?dswid=7662
"""

import numpy as np

from ....format import make_array_method
from ...general import SaturatedSolutionFormula


class Solubility_CRCHandbook_Base(SaturatedSolutionFormula):

    source = 'CRC Handbook'

    concentration_unit = 'm'
    temperature_unit = 'C'

    def calculate(self, T):
        a0, a1, a2 = self.coeffs
        return a0 + a1 * T + a2 * T**2


# =============================== Steiger 2008 ===============================


class Solubility_NaCl_CRCHandbook_Base(Solubility_CRCHandbook_Base):
    crystal = 'NaCl'
    temperature_range = (10, 40)
    coeffs = 6.09457143, 9.47619048e-4, 5.61904762e-5


class Solubility_LiCl_CRCHandbook_Base(Solubility_CRCHandbook_Base):
    crystal = 'LiCl'
    temperature_range = (10, 25)
    coeffs = 19.13215, 5.87e-03, 1.05e-3
