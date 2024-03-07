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

from .misc import aw_extended_debye_huckel
from ..steiger import coeffs_steiger_2008
from ..pitzer import PitzerActivity
from ...general import SolutionFormula

class WaterActivity_KCl_Steiger2008(SolutionFormula):

    name = 'Steiger 2008'
    solute = 'KCl'

    temperature_unit = 'K'
    temperature_range = (278.15, 323.15)   # NOT SURE (see above)

    concentration_unit = 'm'
    concentration_range = (0, 15)  # NOT SURE (see above)

    default = True
    with_water_reference = False

    def calculate(self, m, T):
        coeffs = coeffs_steiger_2008.coeffs(solute='KCl', T=T)
        pitz = PitzerActivity(T=T, solute='KCl', **coeffs)
        return pitz.water_activity(m=m)


class WaterActivity_KCl_Tang(SolutionFormula):

    name = 'Tang'
    solute = 'KCl'

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'm'
    concentration_range = (1e-9, 13)

    with_water_reference = False

    coeffs = {
        'A': 0.5108,
        'B': 1.35,
        'C': 7.625e-3,
        'D': -7.892e-4,
        'E': 2.492e-5,
        'beta': -9.842e-3,
    }

    def calculate(self, m, T):
        coeffs_tang_KCl = self.coeffs.values()
        return aw_extended_debye_huckel(m, T, solute='KCl', coeffs=coeffs_tang_KCl)


# ========================== WRAP-UP OF FORMULAS =============================

WaterActivityFormulas_KCl = (
    WaterActivity_KCl_Steiger2008,
    WaterActivity_KCl_Tang,
)