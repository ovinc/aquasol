"""Gathers the formulas for the viscosity of LiCl solutions.

Sources
-------
--- Mao, S. & Duan, Z.
    The Viscosity of Aqueous Alkali-Chloride Solutions up to 623 K, 1,000 bar,
    and High Ionic Strength.
    Int J Thermophys 30, 1510-1523 (2009).
"""

from .maoduan import Viscosity_MaoDuan_LiCl_Base


class Viscosity_LiCl_MaoDuan(Viscosity_MaoDuan_LiCl_Base):
    """Already defined in maoduan module"""
    default = True


# ========================== WRAP-UP OF FORMULAS =============================

ViscosityFormulas_LiCl = (
    Viscosity_LiCl_MaoDuan,
)
