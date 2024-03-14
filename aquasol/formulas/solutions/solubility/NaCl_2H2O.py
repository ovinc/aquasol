"""Gathers the formulas for the solubility of NaCl,2H2O solutions.


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
"""

from .steiger import Solubility_NaCl_2H2O_Steiger2008_Base


class Solubility_NaCl_2H2O_Steiger(Solubility_NaCl_2H2O_Steiger2008_Base):
    """Already defined in steiger module"""
    default = True


# ============================= WRAP-UP FORMULAS =============================

SolubilityFormulas_NaCl_2H2O = (
    Solubility_NaCl_2H2O_Steiger,
)