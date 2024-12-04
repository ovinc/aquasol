"""Gathers the formulas for the refractive index of NaCl solutions.

See tang.py and tan.py modules for more info.
"""

from .tan import RefractiveIndex_NaCl_Tan_Base
from .tang import RefractiveIndex_NaCl_Tang_Base


class RefractiveIndex_NaCl_Tan(RefractiveIndex_NaCl_Tan_Base):
    """Already defined in tan module"""
    default = True


class RefractiveIndex_NaCl_Tang(RefractiveIndex_NaCl_Tang_Base):
    """Already defined in tang module and not default."""
    pass


# ============================= WRAP-UP FORMULAS =============================

RefractiveIndexFormulas_NaCl = (
    RefractiveIndex_NaCl_Tan,
    RefractiveIndex_NaCl_Tang,
)
