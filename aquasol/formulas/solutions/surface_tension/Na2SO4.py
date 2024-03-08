"""Gathers the formulas for the surface tension of Na2SO4 solutions.

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
- Dutcher: Dutcher, C. S., Wexler, A. S. & Clegg, S. L. Surface Tensions of
Inorganic Multicomponent Aqueous Electrolyte Solutions and Melts.
J. Phys. Chem. A 114, 12216-12230 (2010).
"""

from .dutcher import SufaceTension_Na2SO4_Dutcher_Base


class SurfaceTension_Na2SO4_Dutcher(SufaceTension_Na2SO4_Dutcher_Base):
    """Already defined in dutcher module"""
    default = True


# ========================== WRAP-UP OF FORMULAS =============================

SurfaceTensionFormulas_Na2SO4 = (
    SurfaceTension_Na2SO4_Dutcher,
)

