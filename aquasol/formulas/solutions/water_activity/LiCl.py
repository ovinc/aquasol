"""Gathers the formulas for the activity of LiCl solutions.

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
- Conde, M. R., Properties of aqueous solutions of lithium and calcium
chlorides: formulations for use in air conditioning equipment design.
International Journal of Thermal Sciences 43, 367-382 (2004).
"""

# TODO: add Gibbard 1973 and/or Patil 1990? (maybe do not have as many
# problems as Conde near w = 0)

from .misc import aw_conde
from ...general import SolutionFormula


class WaterActivity_LiCl_Conde(SolutionFormula):

    name = 'Conde'
    solute = 'LiCl'

    temperature_unit = 'C'
    temperature_range = (0, 100)   # Deduced from data presented in Fig. 3

    concentration_unit = 'w'
    # Approximative, actually depends on temperature. Conde not defined in w=0 ...
    concentration_range = (0.00001, 0.55)

    default = True
    with_water_reference = False

    coeffs = [
        0.28,
        4.30,
        0.6,
        0.21,
        5.1,
        0.49,
        0.362,
        -4.75,
        -0.4,
        0.03,
    ]

    def calculate(self, w, T):
        """Water activity for LiCl as a function of concentration according to Conde."""
        T = T + 273.15
        aw = aw_conde(w, T, self.coeffs)
        return aw


# ========================== WRAP-UP OF FORMULAS =============================

WaterActivityFormulas_LiCl = (
    WaterActivity_LiCl_Conde,
)