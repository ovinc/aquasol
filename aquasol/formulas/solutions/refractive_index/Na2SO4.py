"""Gathers the formulas for the refractive index of Na2SO4 solutions.

See tang.py module for more info.
"""

from .tang import RefractiveIndex_Na2SO4_Tang_Base


class RefractiveIndex_Na2SO4_Tang(RefractiveIndex_Na2SO4_Tang_Base):
    """Already defined in tang module"""
    default = True


# ============================= WRAP-UP FORMULAS =============================

RefractiveIndexFormulas_Na2SO4 = (
    RefractiveIndex_Na2SO4_Tang,
)
