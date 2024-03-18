"""Gathers the formulas for the activity of LiBr solutions.

Sources
-------
- Pitzer, K. S. & Mayorga, G.
  Thermodynamics of electrolytes. II.
  Activity and osmotic coefficients for strong electrolytes with one or both
  ions univalent.
  J. Phys. Chem. 77, 2300-2308
  (1973)
"""

from .patil import WaterActivity_LiBr_Patil_Base
from .pitzer import WaterActivity_LiBr_Pitzer_Base


class WaterActivity_LiBr_Patil(WaterActivity_LiBr_Patil_Base):
    """Already defined in pitzer module"""
    default = True


class WaterActivity_LiBr_Pitzer(WaterActivity_LiBr_Pitzer_Base):
    """Already defined in pitzer module"""
    pass



# ========================== WRAP-UP OF FORMULAS =============================

WaterActivityFormulas_LiBr = (
    WaterActivity_LiBr_Patil,
    WaterActivity_LiBr_Pitzer,
)
