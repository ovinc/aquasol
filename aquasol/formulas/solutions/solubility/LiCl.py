"""Gathers the formulas for the solubility of LiCl solutions.

Sources
-------
- CRC Handbook of Chemistry and Physics, 104th Edition
  Section: 4 | Solubility of Common Inorganic Salts as a Function of Temperature
  https://hbcp.chemnetbase.com/documents/04_29/04_29_0001.xhtml?dswid=7662
"""

from .crc_handbook import Solubility_LiCl_CRCHandbook_Base


class Solubility_LiCl_CRCHandbook(Solubility_LiCl_CRCHandbook_Base):
    """Already defined in CRC Handbook module"""
    default = True


# ============================= WRAP-UP FORMULAS =============================

SolubilityFormulas_LiCl = (
    Solubility_LiCl_CRCHandbook,
)