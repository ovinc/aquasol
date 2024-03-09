"""Gathers the formulas for the density of LiCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns two parameters:
- rho0, density of pure water in kg / m^3
- rho, density of solution in kg / m^3
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
- Conde, M. R., Properties of aqueous solutions of lithium and calcium
  chlorides: formulations for use in air conditioning equipment design.
  International Journal of Thermal Sciences 43, 367-382 (2004).

- Krumgalz, B. S., Pogorelsky, R. & Pitzer, K. S.
  Volumetric Properties of Single Aqueous Electrolytes from Zero to Saturation
  Concentration at 298.15 °K Represented by Pitzer's Ion-Interaction Equations.
  Journal of Physical and Chemical Reference Data 25, 663-689 (1996).
"""

from ...general import SolutionFormula
from ...water.density_atm import DensityAtm_IAPWS

from .misc import relative_rho_conde
from .krumgalz import Density_LiCl_Krumgalz_Base

class Density_LiCl_Conde(SolutionFormula):

    source ='Conde'
    solute = 'LiCl'

    temperature_unit = 'K'
    temperature_range = (273.15, 373.15)

    concentration_unit = 'r'
    concentration_range = (0, 1.273)

    default = True
    with_water_reference = True

    coeffs = 1, 0.540966, -0.303792, 0.100791

    def calculate(self, z, T):
        d = relative_rho_conde(z, self.coeffs)
        density_atm = DensityAtm_IAPWS()
        rho0 = density_atm.calculate(T=T)
        return rho0, rho0 * d


class Density_LiCl_Krumgalz(Density_LiCl_Krumgalz_Base):
    """Already defined in Krumgalz module and not default here"""
    pass


# ========================== WRAP-UP OF FORMULAS =============================

Density_LiCl_Formulas = (
    Density_LiCl_Conde,
    Density_LiCl_Krumgalz
)