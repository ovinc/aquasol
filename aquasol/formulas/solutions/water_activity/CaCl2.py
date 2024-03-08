"""Gathers the formulas for the activity of CaCl2 solutions.

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


from .conde import WaterActivity_CaCl2_Conde_Base


class WaterActivity_CaCl2_Conde(WaterActivity_CaCl2_Conde_Base):
    """Already defined in conde module"""
    default = True


# ========================== WRAP-UP OF FORMULAS =============================

WaterActivityFormulas_CaCl2 = (
    WaterActivity_CaCl2_Conde,
)
