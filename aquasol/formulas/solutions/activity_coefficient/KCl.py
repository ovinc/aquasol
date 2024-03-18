"""Gathers the formulas for the activity coefficients of KCl solutions.

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
