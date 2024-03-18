"""Gathers the formulas for the activity coefficients of LiBr solutions.

Sources
-------

Pitzer, K. S. & Mayorga, G.
Thermodynamics of electrolytes. II.
Activity and osmotic coefficients for strong electrolytes with one or both
ions univalent.
J. Phys. Chem. 77, 2300-2308
(1973)
"""

from .pitzer import ActivityCoefficient_LiBr_Pitzer_Base


class ActivityCoefficient_LiBr_Pitzer(ActivityCoefficient_LiBr_Pitzer_Base):
    """Already defined in pitzer module"""
    default = True


# ========================== WRAP-UP OF FORMULAS =============================

ActivityCoefficientFormulas_LiBr = (
    ActivityCoefficient_LiBr_Pitzer,
)
