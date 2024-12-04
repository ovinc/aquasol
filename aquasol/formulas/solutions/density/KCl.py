"""Gathers the formulas for the density of KCl solutions.

see al_ghafri.py, krumgalz.py, tang.py moduled for more info
"""

from .al_ghafri import Density_KCl_AlGhafri_Base
from .krumgalz import Density_KCl_Krumgalz_Base
from .tang import Density_KCl_Tang_Base


class Density_KCl_AlGhafri(Density_KCl_AlGhafri_Base):
    """Already defined in Al Ghafri module"""
    default = True


class Density_KCl_Krumgalz(Density_KCl_Krumgalz_Base):
    """Already defined in Krumgalz module and not default here"""
    pass


class Density_KCl_Tang(Density_KCl_Tang_Base):
    """Already defined in Tang module and not default here"""
    pass


# ========================== WRAP-UP OF FORMULAS =============================

Density_KCl_Formulas = (
    Density_KCl_AlGhafri,
    Density_KCl_Krumgalz,
    Density_KCl_Tang,
)
