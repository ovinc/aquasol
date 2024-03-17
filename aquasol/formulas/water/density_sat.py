"""Function to calculate the density of saturated water as a function of
temperature using IAPWS recommended equation and others.

Sources
-------

--- 'IAPWS'
    Wagner and Pruß
    "The IAPWS Formulation 1995 for the Thermodynamic Properties of Ordinary
    Water Substance for General and Scientific Use"
    (2002)
    Equation 2.6 page 399

--- 'Conde'
    Conde, M. R.
    Properties of aqueous solutions of lithium and calcium chlorides:
    formulations for use in air conditioning equipment design.
    International Journal of Thermal Sciences 43, 367-382
    (2004)
"""

from ...constants import Tc, rhoc
from ..general import WaterFormula


class DensitySat_IAPWS(WaterFormula):

    source ='IAPWS'
    temperature_unit = 'K'
    temperature_range = (273.15, Tc)
    default = True

    coeffs = [
        1.99274064,
        1.09965342,
        -0.510839303,
        -1.75493479,
        -45.5170352,
        -6.74694450e5,
    ]

    def calculate(self, T):
        """Saturated water density according to Wagner and Pruss 2002 (IAPWS 95)

        Input
        -----
        Temperature in K

        Output
        ------
        Density in kg/m^3

        Reference
        ---------
        Wagner and Pruß : "The IAPWS Formulation 1995 for the Thermodynamic Properties
        of Ordinary Water Substance for General and Scientific Use" (2002), eq. (2.6)

        Notes
        -----
        - Used by Al Ghafri 2012
        - Valid between triple point (0.01°C) and critical temperature 647.096K
        """
        c1, c2, c3, c4, c5, c6 = self.coeffs
        phi = 1 - T / Tc
        rho = rhoc * (1 + c1 * phi**(1/3) + c2 * phi**(2/3) + c3 * phi**(5/3)
                        + c4 * phi**(16/3) + c5 * phi**(43/3) + c6 * phi**(110/3))
        return rho


class DensitySat_Conde(WaterFormula):

    source ='Conde'
    temperature_unit = 'K'
    temperature_range = (273.15, Tc)

    coeffs = [
        1.9937718430,
        1.0985211604,
        -0.5094492996,
        -1.7619124270,
        -44.9005480267,
        -723692.2618632,
    ]

    def calculate(self, T):
        """Water density equation that looks very similar to Wagner, used by Conde.

        Input
        -----
        Temperature in C

        Output
        ------
        Density in kg/m^3

        Reference
        ---------
        Conde, M. R., Properties of aqueous solutions of lithium and calcium
        chlorides: formulations for use in air conditioning equipment design.
        International Journal of Thermal Sciences 43, 367-382 (2004).

        """
        c1, c2, c3, c4, c5, c6 = self.coeffs
        phi = 1 - T / Tc
        rho = rhoc * (1 + c1 * phi**(1/3) + c2 * phi**(2/3) + c3 * phi**(5/3)
                        + c4 * phi**(16/3) + c5 * phi**(43/3) + c6 * phi**(110/3))
        return rho


# ========================== WRAP-UP OF FORMULAS =============================

DensitySatFormulas = (
    DensitySat_IAPWS,
    DensitySat_Conde
)
