"""Steiger formulas for the activity coefficients of solutions.

NOTE: Almost identical in structure to water_activity.steiger

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
"""

from ...general import SolutionFormula
from ..steiger import coeffs_steiger2005_activity, coeffs_steiger2008_activity
from ..pitzer import PitzerActivity


steiger_coeffs = {
    'Steiger 2005': coeffs_steiger2005_activity,
    'Steiger 2008': coeffs_steiger2008_activity,
}


class ActivityCoefficient_Steiger_Base(SolutionFormula):

    temperature_unit = 'K'
    concentration_unit = 'm'

    with_water_reference = False

    def calculate(self, m, T):
        coeffs = steiger_coeffs[self.source].coeffs(solute=self.solute, T=T)
        pitz = PitzerActivity(T=T, solute=self.solute, **coeffs)
        return pitz.activity_coefficient(m=m)


# =============================== Steiger 2005 ===============================


class ActivityCoefficient_Steiger2005_Base(ActivityCoefficient_Steiger_Base):
    source ='Steiger 2005'
    temperature_range = (298.15, 298.15)


class ActivityCoefficient_NaCl_Steiger2005_Base(ActivityCoefficient_Steiger2005_Base):
    solute = 'NaCl'
    concentration_range = (0, 13.5)


class ActivityCoefficient_Na2SO4_Steiger2005_Base(ActivityCoefficient_Steiger2005_Base):
    solute = 'Na2SO4'
    concentration_range = (0, 12)


# =============================== Steiger 2008 ===============================


class ActivityCoefficient_Steiger2008_Base(ActivityCoefficient_Steiger_Base):
    source ='Steiger 2008'
    temperature_range = (273.15, 323.15)


class ActivityCoefficient_NaCl_Steiger2008_Base(ActivityCoefficient_Steiger2008_Base):
    solute = 'NaCl'
    concentration_range = (0, 15)


class ActivityCoefficient_Na2SO4_Steiger2008_Base(ActivityCoefficient_Steiger2008_Base):
    solute = 'Na2SO4'
    concentration_range = (0, 12)


class ActivityCoefficient_KCl_Steiger2008_Base(ActivityCoefficient_Steiger2008_Base):
    solute = 'KCl'
    concentration_range = (0, 15)  # NOT SURE (see above)
