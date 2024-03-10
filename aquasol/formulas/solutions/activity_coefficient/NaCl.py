"""Gathers the formulas for the activity coefficients of NaCl solutions.

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

(some info of domain of validity of expressions in the following paper:)
Dorn, J. & Steiger, M. Measurement and Calculation of Solubilities in the
Ternary System NaCH 3 COO + NaCl + H 2 O from 278 K to 323 K.
J. Chem. Eng. Data 52, 1784-1790 (2007).)

- Tang, I. N., Munkelwitz, H. R. & Wang, N.
  Water activity measurements with single suspended droplets:
  The NaCl-H2O and KCl-H2O systems.
  Journal of Colloid and Interface Science 114, 409-415 (1986).
  Valid at 25°C and for solutions of molality up to ~13 mol/kg
"""

from .steiger import ActivityCoefficient_NaCl_Steiger2005_Base
from .steiger import ActivityCoefficient_NaCl_Steiger2008_Base
from .tang import ActivityCoefficient_NaCl_Tang_Base


class ActivityCoefficient_NaCl_Tang(ActivityCoefficient_NaCl_Tang_Base):
    """Already defined in tang module"""
    pass

class ActivityCoefficient_NaCl_Steiger2005(ActivityCoefficient_NaCl_Steiger2005_Base):
    """Already defined in steiger module"""
    pass


class ActivityCoefficient_NaCl_Steiger2008(ActivityCoefficient_NaCl_Steiger2008_Base):
    """Already defined in steiger module"""
    default = True


# ============================= WRAP-UP FORMULAS =============================

ActivityCoefficientFormulas_NaCl = (
    ActivityCoefficient_NaCl_Steiger2008,
    ActivityCoefficient_NaCl_Steiger2005,
    ActivityCoefficient_NaCl_Tang,
)