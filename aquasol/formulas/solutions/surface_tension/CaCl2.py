"""Gathers the formulas for the surface tension of CaCl2 solutions.

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
- Conde, M. R., Properties of aqueous solutions of lithium and calcium
chlorides: formulations for use in air conditioning equipment design.
International Journal of Thermal Sciences 43, 367-382 (2004).

- Dutcher: Dutcher, C. S., Wexler, A. S. & Clegg, S. L. Surface Tensions of
Inorganic Multicomponent Aqueous Electrolyte Solutions and Melts.
J. Phys. Chem. A 114, 12216-12230 (2010).
"""

from .dutcher import SufaceTension_CaCl2_Dutcher_Base
from .conde import SurfaceTension_CaCl2_Conde_Base


class SurfaceTension_CaCl2_Dutcher(SufaceTension_CaCl2_Dutcher_Base):
    """Already defined in dutcher module"""
    default = True


class SurfaceTension_CaCl2_Conde(SurfaceTension_CaCl2_Conde_Base):
    """Already defined in conde module"""
    pass


# ========================== WRAP-UP OF FORMULAS =============================

SurfaceTensionFormulas_CaCl2 = (
    SurfaceTension_CaCl2_Dutcher,
    SurfaceTension_CaCl2_Conde,
)
