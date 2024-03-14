"""Gathers the formulas for the solubility of NaCl solutions.

Sources
-------
- Steiger, M., Kiekbusch, J. & Nicolai,
  An improved model incorporating Pitzer's equations for calculation of
  thermodynamic properties of pore solutions implemented into an efficient
  program code.
  Construction and Building Materials 22, 1841-1850 (2008).

(some info of domain of validity of expressions in the following paper:)
Dorn, J. & Steiger, M. Measurement and Calculation of Solubilities in the
Ternary System NaCH 3 COO + NaCl + H 2 O from 278 K to 323 K.
J. Chem. Eng. Data 52, 1784-1790 (2007).)

- CRC Handbook of Chemistry and Physics, 104th Edition
  Section: 4 | Solubility of Common Inorganic Salts as a Function of Temperature
  https://hbcp.chemnetbase.com/documents/04_29/04_29_0001.xhtml?dswid=7662

- Sparrow, B. S.
  Empirical equations for the thermodynamic properties of aqueous sodium chloride. Desalination 159, 161-170
  (2003).
"""

from ...general import SaturatedSolutionFormula
from .steiger import Solubility_NaCl_Steiger2008_Base
from .crc_handbook import Solubility_NaCl_CRCHandbook_Base


class Solubility_NaCl_Steiger(Solubility_NaCl_Steiger2008_Base):
    """Already defined in steiger module"""
    default = True


class Solubility_NaCl_CRCHandbook(Solubility_NaCl_CRCHandbook_Base):
    """Already defined in CRC Handbook module"""
    pass


class Solubility_NaCl_Sparrow(SaturatedSolutionFormula):

    source = 'Sparrow'
    crystal = 'NaCl'

    temperature_unit = 'C'
    temperature_range = (0, 450)

    concentration_unit = 'w'

    coeffs = 0.2628, 62.75e-6, 1.084e-6

    def calculate(self, T):
        a0, a1, a2 = self.coeffs
        return a0 + a1 * T + a2 * T**2


# ============================= WRAP-UP FORMULAS =============================

SolubilityFormulas_NaCl = (
    Solubility_NaCl_Steiger,
    Solubility_NaCl_CRCHandbook,
    Solubility_NaCl_Sparrow
)