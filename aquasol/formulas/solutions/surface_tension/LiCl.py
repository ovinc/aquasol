"""Gathers the formulas for the surface tension of LiCl solutions.

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
"""


from .conde import SurfaceTension_LiCl_Conde_Base


class SurfaceTension_LiCl_Conde(SurfaceTension_LiCl_Conde_Base):
    """Already defined in conde module"""
    default = True


# ========================== WRAP-UP OF FORMULAS =============================

SurfaceTensionFormulas_LiCl = (
    SurfaceTension_LiCl_Conde,
)

