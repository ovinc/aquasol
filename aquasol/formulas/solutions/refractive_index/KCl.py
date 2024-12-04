"""Gathers the formulas for the refractive index of KCl solutions.

See tang.py and tan.py modules for more info.
"""

from .tan import RefractiveIndex_KCl_Tan_Base
from .tang import RefractiveIndex_KCl_Tang_Base


class RefractiveIndex_KCl_Tan(RefractiveIndex_KCl_Tan_Base):
    """Already defined in tan module"""
    default = True


class RefractiveIndex_KCl_Tang(RefractiveIndex_KCl_Tang_Base):
    """Already defined in tang module and not default here"""
    pass


# ============================= WRAP-UP FORMULAS =============================

RefractiveIndexFormulas_KCl = (
    RefractiveIndex_KCl_Tan,
    RefractiveIndex_KCl_Tang,
)
