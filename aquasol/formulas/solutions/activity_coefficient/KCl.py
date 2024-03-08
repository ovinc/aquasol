"""Gathers the formulas for the activity coefficients of KCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns one parameter
- gamma, molal activity coefficient (dimensionless)
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------

- Steiger, M., Kiekbusch, J. & Nicolai,
  An improved model incorporating Pitzer's equations for calculation of
  thermodynamic properties of pore solutions implemented into an efficient
  program code.
  Construction and Building Materials 22, 1841-1850 (2008).

NOTE: I could not find explicit info about validity domain for the KCl
      formulas in Steiger, so I kept ~ same values as for NaCl
"""

from .steiger import ActivityCoefficient_KCl_Steiger2008_Base
from .tang import ActivityCoefficient_KCl_Tang_Base


class ActivityCoefficient_KCl_Steiger2008(ActivityCoefficient_KCl_Steiger2008_Base):
    """Already defined in steiger module"""
    default = True


class ActivityCoefficient_KCl_Tang(ActivityCoefficient_KCl_Tang_Base):
    """Already defined in tang module"""
    pass


# ========================== WRAP-UP OF FORMULAS =============================

ActivityCoefficientFormulas_KCl = (
    ActivityCoefficient_KCl_Steiger2008,
    ActivityCoefficient_KCl_Tang,
)
