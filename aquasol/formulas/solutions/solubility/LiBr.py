"""Gathers the formulas for the solubility of LiBr solutions.

Sources
-------
--- Duvall
Duvall, K. N., Dirksen, J. A. & Ring, T. A.
Ostwald-Meyers Metastable Region in LiBr Crystallization—Comparison of
Measurements with Predictions.
Journal of Colloid and Interface Science 239, 391-398
(2001)
"""

from .duvall import Solubility_LiBr_1H2O_Duvall_Base
from .duvall import Solubility_LiBr_2H2O_Duvall_Base
from .duvall import Solubility_LiBr_3H2O_Duvall_Base


class Solubility_LiBr_1H2O_Duvall(Solubility_LiBr_1H2O_Duvall_Base):
    """Default for monohydrate"""
    default = True


class Solubility_LiBr_2H2O_Duvall(Solubility_LiBr_2H2O_Duvall_Base):
    """Default for monohydrate"""
    default = True


class Solubility_LiBr_3H2O_Duvall(Solubility_LiBr_3H2O_Duvall_Base):
    """Default for monohydrate"""
    default = True


# ============================= WRAP-UP FORMULAS =============================

SolubilityFormulas_LiBr = (
    Solubility_LiBr_1H2O_Duvall,
    Solubility_LiBr_2H2O_Duvall,
    Solubility_LiBr_3H2O_Duvall,
)
