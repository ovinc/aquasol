"""Gathers the formulas for the activity coefficients of LiCl solutions.

Sources
-------

Pitzer, K. S. & Mayorga, G.
Thermodynamics of electrolytes. II.
Activity and osmotic coefficients for strong electrolytes with one or both
ions univalent.
J. Phys. Chem. 77, 2300-2308
(1973)
"""

from .pitzer import ActivityCoefficient_LiCl_Pitzer_Base


class ActivityCoefficient_LiCl_Pitzer(ActivityCoefficient_LiCl_Pitzer_Base):
    """Already defined in pitzer module"""
    default = True


# ========================== WRAP-UP OF FORMULAS =============================

ActivityCoefficientFormulas_LiCl = (
    ActivityCoefficient_LiCl_Pitzer,
)
