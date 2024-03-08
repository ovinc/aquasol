"""Gathers the formulas for the activity of Na2SO4 solutions.

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
- Clegg et al. : "Thermodynamic Properties of Aqueous Aerosols to High
Supersaturation: II" (1997). Valid at 25°C and for solutions of molality
up to ~17 mol/kg (x ~ 0.23)

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

For now, I have assumed validity similar to NaCl (in temperatures)
"""

from .clegg import WaterActivity_Na2SO4_Clegg_Base
from .steiger import WaterActivity_Na2SO4_Steiger2005_Base
from .steiger import WaterActivity_Na2SO4_Steiger2008_Base


class WaterActivity_Na2SO4_Steiger2005(WaterActivity_Na2SO4_Steiger2005_Base):
    """Already defined in steiger module"""
    pass


class WaterActivity_Na2SO4_Steiger2008(WaterActivity_Na2SO4_Steiger2008_Base):
    """Already defined in steiger module"""
    default = True

class WaterActivity_Na2SO4_Clegg(WaterActivity_Na2SO4_Clegg_Base):
    """Already defined in clegg module"""
    pass


# ========================== WRAP-UP OF FORMULAS =============================

WaterActivityFormulas_Na2SO4 = (
    WaterActivity_Na2SO4_Steiger2008,
    WaterActivity_Na2SO4_Steiger2005,
    WaterActivity_Na2SO4_Clegg,
)
