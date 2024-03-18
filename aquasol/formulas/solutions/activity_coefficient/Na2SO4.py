"""Gathers the formulas for the activity coefficients of Na2SO4 solutions.

Sources
-------

- Steiger, M.,
  Crystal growth in porous materials—I:
  The crystallization pressure of large crystals.
  Journal of Crystal Growth 282, 455-469 (2005).
  Valid at 25°C and up to 13.5 mol/kg

- Steiger, M., Kiekbusch, J. & Nicolai,
  An improved model incorporating Pitzer's equations for calculation of
  thermodynamic properties of pore solutions implemented into an efficient
  program code.
  Construction and Building Materials 22, 1841-1850 (2008).

Note: some potential info about validity in:
Steiger, M. & Asmussen, S.
Crystallization of sodium sulfate phases in porous materials:
The phase diagram Na2SO4-H2O and the generation of stress.
Geochimica et Cosmochimica Acta 72, 4291-4306 (2008).

For now, I have assumed validity similar to NaCl (in temperatures)
"""

from .steiger import ActivityCoefficient_Na2SO4_Steiger2005_Base
from .steiger import ActivityCoefficient_Na2SO4_Steiger2008_Base


class ActivityCoefficient_Na2SO4_Steiger2005(ActivityCoefficient_Na2SO4_Steiger2005_Base):
    """Already defined in steiger module"""
    pass


class ActivityCoefficient_Na2SO4_Steiger2008(ActivityCoefficient_Na2SO4_Steiger2008_Base):
    """Already defined in steiger module"""
    default = True


# ========================== WRAP-UP OF FORMULAS =============================

ActivityCoefficientFormulas_Na2SO4 = (
    ActivityCoefficient_Na2SO4_Steiger2008,
    ActivityCoefficient_Na2SO4_Steiger2005,
)
