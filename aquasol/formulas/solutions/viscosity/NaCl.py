"""Gathers the formulas for the viscosity of NaCl solutions.

Sources
-------
--- Mao, S. & Duan, Z.
    The Viscosity of Aqueous Alkali-Chloride Solutions up to 623 K, 1,000 bar,
    and High Ionic Strength.
    Int J Thermophys 30, 1510-1523 (2009).
"""

# TODO: add data from Simion

from .maoduan import Viscosity_MaoDuan_NaCl_Base


class Viscosity_NaCl_MaoDuan(Viscosity_MaoDuan_NaCl_Base):
    """Already defined in maoduan module"""
    default = True


# ========================== WRAP-UP OF FORMULAS =============================

ViscosityFormulas_NaCl = (
    Viscosity_NaCl_MaoDuan,
)
