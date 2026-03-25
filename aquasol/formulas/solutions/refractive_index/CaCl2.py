"""Gathers the formulas for the refractive index of KCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns one parameter:
- n (index of refraction, dimensionless)
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
- Tan (default) : "Dependence of Refractive Index on Concentration and
Temperature in Electrolyte Solution, Polar Solution, Nonpolar Solution, and
Protein Solution", Tan & Huang, J. Chem. Eng. Data  (2015).
Valid from w = 0 to w = 0.25 and for temperatures between 20 and 45°C
"""

from .tan import RefractiveIndex_CaCl2_Tan_Base


class RefractiveIndex_CaCl2_Tan(RefractiveIndex_CaCl2_Tan_Base):
    """Already defined in tan module"""
    default = True


# ============================= WRAP-UP FORMULAS =============================

RefractiveIndexFormulas_CaCl2 = (
    RefractiveIndex_CaCl2_Tan,
)
