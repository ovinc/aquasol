"""Gathers the formulas for the activity of KCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns one parameter
- a, water activity (dimensionless, range 0-1)
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
- Tang, I. N., Munkelwitz, H. R. & Wang, N.
  Water activity measurements with single suspended droplets:
  The NaCl-H2O and KCl-H2O systems.
  Journal of Colloid and Interface Science 114, 409-415 (1986).
  Valid at 25°C and for solutions of molality up to ~13 mol/kg

- Steiger, M., Kiekbusch, J. & Nicolai,
  An improved model incorporating Pitzer's equations for calculation of
  thermodynamic properties of pore solutions implemented into an efficient
  program code.
  Construction and Building Materials 22, 1841-1850 (2008).

NOTE: I could not find explicit info about validity domain for the KCl
      formulas in Steiger, so I kept ~ same values as for NaCl
"""

from .steiger import WaterActivity_KCl_Steiger2008_Base
from .tang import WaterActivity_KCl_Tang_Base


class WaterActivity_KCl_Steiger2008(WaterActivity_KCl_Steiger2008_Base):
    """Already defined in steiger module"""
    default = True


class WaterActivity_KCl_Tang(WaterActivity_KCl_Tang_Base):
    """Already defined in tang module"""
    pass


# ========================== WRAP-UP OF FORMULAS =============================

WaterActivityFormulas_KCl = (
    WaterActivity_KCl_Steiger2008,
    WaterActivity_KCl_Tang,
)
