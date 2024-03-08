"""Gathers the formulas for the surface tension of NaCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns two parameters
- sigma0, sigma surface tensions in N/m of pure water and solution
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
- Dutcher: Dutcher, C. S., Wexler, A. S. & Clegg, S. L.
  Surface Tensions of Inorganic Multicomponent Aqueous Electrolyte Solutions and Melts.
  J. Phys. Chem. A 114, 12216-12230 (2010).

- Talreja-Muthreja, T., Linnow, K., Enke, D. & Steiger
  M. Deliquescence of NaCl Confined in Nanoporous Silica.
  Langmuir 38, 10963-10974 (2022).
"""

# TODO: add data from Ali 2006

from ...general import SolutionFormula
from .dutcher import SufaceTension_NaCl_Dutcher_Base
from .misc import sigma_iapws


class SurfaceTension_NaCl_Dutcher(SufaceTension_NaCl_Dutcher_Base):
    """Already defined in dutcher module"""
    default = True


class SurfaceTension_NaCl_Steiger(SolutionFormula):

    source ='Steiger'
    solute = 'NaCl'

    temperature_unit = 'C'
    temperature_range = (-10, 50)

    concentration_unit = 'm'
    concentration_range = (0, 7)     # approx (up to saturation)

    with_water_reference = True

    def calculate(self, m, T):
        """Surface tension calculated from Talreja-Muthreja et al. 2022
        Input: molality m, temperature T in Celsius."""
        sigma_w = sigma_iapws(T + 273.15)
        sigma = sigma_w + 0.00166 * m
        return sigma_w, sigma


# ========================== WRAP-UP OF FORMULAS =============================

SurfaceTensionFormulas_NaCl = (
    SurfaceTension_NaCl_Dutcher,
    SurfaceTension_NaCl_Steiger,
)