"""Activity of solutions from Conde 2004

Source
------
- Conde, M. R., Properties of aqueous solutions of lithium and calcium
chlorides: formulations for use in air conditioning equipment design.
International Journal of Thermal Sciences 43, 367-382 (2004).
"""

import numpy as np

from ....constants import Tc
from ...general import SolutionFormula


def aw_conde(w, T, coeffs):
    """General formula for surface tension accorging to Conde IJTS 2004.

    Inputs
    ------
    w: weight fraction of salt
    T: temperature in K
    coeffs: coeffs pi_i from Table 3

    Outputs
    -------
    Water activity of solution (dimensionless)

    Notes
    -----
    The expression does not tend to 1 at 0 concentration and is not defined
    for w=0 !!

    Reference
    ---------
    Conde, M. R., Properties of aqueous solutions of lithium and calcium
    chlorides: formulations for use in air conditioning equipment design.
    International Journal of Thermal Sciences 43, 367-382 (2004).
    """
    pi0, pi1, pi2, pi3, pi4, pi5, pi6, pi7, pi8, pi9 = coeffs

    a = 2 - (1 + (w / pi0)**pi1)**pi2
    b = (1 + (w / pi3)**pi4)**pi5 - 1

    t = T / Tc

    f = a + b * t
    pi25 = 1 - (1 + (w / pi6)**pi7)**pi8 - pi9 * np.exp(-(w - 0.1)**2 / 0.005)

    return f * pi25


class WaterActivity_Conde_Base(SolutionFormula):

    source ='Conde'
    solute = 'CaCl2'

    temperature_unit = 'C'
    temperature_range = (0, 100)   # Deduced from data presented in Fig. 3

    concentration_unit = 'w'

    with_water_reference = False

    def calculate(self, w, T):
        """Water activity for LiCl as a function of concentration according to Conde."""
        T = T + 273.15
        aw = aw_conde(w, T, self.coeffs)
        return aw


class WaterActivity_CaCl2_Conde_Base(WaterActivity_Conde_Base):
        solute = 'CaCl2'
        # Approximative, actually depends on temperature. Conde not defined in w=0 ...
        concentration_range = (1e-9, 0.6)
        coeffs = [0.31, 3.698, 0.6, 0.231, 4.584, 0.49, 0.478, -5.20, -0.4, 0.018]


class WaterActivity_LiCl_Conde_Base(WaterActivity_Conde_Base):
        solute = 'LiCl'
        # Approximative, actually depends on temperature. Conde not defined in w=0 ...
        concentration_range = (1e-9, 0.55)
        coeffs = [0.28, 4.30, 0.6, 0.21, 5.1, 0.49, 0.362, -4.75, -0.4, 0.03]
