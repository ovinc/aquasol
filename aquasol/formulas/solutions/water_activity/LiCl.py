"""Gathers the formulas for the activity of LiCl solutions.

Sources
-------
- Conde, M. R., Properties of aqueous solutions of lithium and calcium
  chlorides: formulations for use in air conditioning equipment design.
  International Journal of Thermal Sciences 43, 367-382 (2004).

- Pitzer, K. S. & Mayorga, G.
  Thermodynamics of electrolytes. II.
  Activity and osmotic coefficients for strong electrolytes with one or both
  ions univalent.
  J. Phys. Chem. 77, 2300-2308
  (1973)
"""

# TODO: add Gibbard 1973 ?

from .conde import WaterActivity_LiCl_Conde_Base
from .patil import WaterActivity_LiCl_Patil_Base
from .pitzer import WaterActivity_LiCl_Pitzer_Base


class WaterActivity_LiCl_Conde(WaterActivity_LiCl_Conde_Base):
    """Already defined in conde module"""
    default = True


class WaterActivity_LiCl_Patil(WaterActivity_LiCl_Patil_Base):
    """Already defined in pitzer module"""
    pass


class WaterActivity_LiCl_Pitzer(WaterActivity_LiCl_Pitzer_Base):
    """Already defined in pitzer module"""
    pass


# ========================== WRAP-UP OF FORMULAS =============================

WaterActivityFormulas_LiCl = (
    WaterActivity_LiCl_Conde,
    WaterActivity_LiCl_Patil,
    WaterActivity_LiCl_Pitzer,
)
