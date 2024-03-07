"""Gathers the formulas for the water activity of NaCl solutions.

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

- Tang, I. N., Munkelwitz, H. R. & Wang, N.
  Water activity measurements with single suspended droplets:
  The NaCl-H2O and KCl-H2O systems.
  Journal of Colloid and Interface Science 114, 409-415 (1986).
  Valid at 25°C and for solutions of molality up to ~13 mol/kg

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

# TODO: add Dutcher (it has supersaturated values!)

from .misc import aw_extended_debye_huckel, aw_clegg
from ..steiger import coeffs_steiger_2005, coeffs_steiger_2008
from ..pitzer import PitzerActivity
from ...general import SolutionFormula


class WaterActivity_NaCl_Clegg(SolutionFormula):

    name = 'Clegg'
    solute = 'NaCl'

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'x'
    concentration_range = (0, 0.25)

    default = True
    with_water_reference = False

    coeffs = {
        'A_x': 2.915,
        'B': 24.22023,
        'alpha': 5.0,
        'W1': 0.7945378,
        'U1': 12.15304,
        'V1': -12.76357,
    }

    def calculate(self, x, T):
        return aw_clegg(x, T, solute='NaCl', coeffs=self.coeffs.values())


class WaterActivity_NaCl_Tang(SolutionFormula):

    name = 'Tang'
    solute = 'NaCl'

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'm'
    concentration_range = (1e-9, 14)

    with_water_reference = False

    coeffs = {
        'A': 0.5108,
        'B': 1.37,
        'C': 4.803e-3,
        'D': -2.736e-4,
        'E': 0,
        'beta': 2.796e-2,
    }

    def calculate(self, m, T):
        return aw_extended_debye_huckel(m, T, solute='NaCl', coeffs=self.coeffs.values())


class WaterActivity_NaCl_Steiger_2005(SolutionFormula):

    name = 'Steiger 2005'
    solute = 'NaCl'

    temperature_unit = 'K'
    temperature_range = (298.15, 298.15)

    concentration_unit = 'm'
    concentration_range = (0, 13.5)

    with_water_reference = False

    def calculate(self, m, T):
        coeffs = coeffs_steiger_2005.coeffs(solute='NaCl', T=T)
        pitz = PitzerActivity(T=T, solute='NaCl', **coeffs)
        return pitz.water_activity(m=m)


class WaterActivity_NaCl_Steiger_2008(SolutionFormula):

    name = 'Steiger 2008'
    solute = 'NaCl'

    temperature_unit = 'K'
    temperature_range = (278.15, 323.15)

    concentration_unit = 'm'
    concentration_range = (0, 15)

    with_water_reference = False

    def calculate(self, m, T):
        coeffs = coeffs_steiger_2008.coeffs(solute='NaCl', T=T)
        pitz = PitzerActivity(T=T, solute='NaCl', **coeffs)
        return pitz.water_activity(m=m)


# ============================= WRAP-UP FORMULAS =============================

WaterActivityFormulas_NaCl = (
    WaterActivity_NaCl_Clegg,
    WaterActivity_NaCl_Tang,
    WaterActivity_NaCl_Steiger_2005,
    WaterActivity_NaCl_Steiger_2008,
)