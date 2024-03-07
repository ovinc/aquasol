"""Gathers the formulas for the density of MgCl2 solutions.

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
- Al Ghafri et al., Densities of Aqueous MgCl2(aq), CaCl2 (aq), KI(aq),
  NaCl(aq), KCl(aq), AlCl3(aq), and (0.964 NaCl + 0.136 KCl)(aq) at
  Temperatures Between (283 and 472) K, Pressures up to 68.5 MPa, and
  Molalities up to 6 mol·kg -1.
  Journal of Chemical & Engineering Data 57, 1288-1304 (2012).

- Krumgalz, B. S., Pogorelsky, R. & Pitzer, K. S.
  Volumetric Properties of Single Aqueous Electrolytes from Zero to Saturation
  Concentration at 298.15 °K Represented by Pitzer's Ion-Interaction Equations.
  Journal of Physical and Chemical Reference Data 25, 663-689 (1996).
"""

from .al_ghafri import Density_MgCl2_AlGhafri_Base
from .krumgalz import Density_MgCl2_Krumgalz_Base


class Density_MgCl2_AlGhafri(Density_MgCl2_AlGhafri_Base):
    """Already defined in Al Ghafri module"""
    default = True


class Density_MgCl2_Krumgalz(Density_MgCl2_Krumgalz_Base):
    """Already defined in Krumgalz module and not default here"""
    pass


# ========================== WRAP-UP OF FORMULAS =============================

Density_MgCl2_Formulas =(
    Density_MgCl2_AlGhafri,
    Density_MgCl2_Krumgalz,
)