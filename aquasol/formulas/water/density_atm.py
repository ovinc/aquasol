"""Function to calculate the desnity of ambient water as a function of
temperature using IAPWS recommended equations or others.

Sources
-------

--- 'IAPWS'
    Patek et al.
    "Reference Correlations for Thermophysical Properties of Liquid Water
    at 0.1 MPa"
    J. Phys. Chem. Ref. Data
    (2009)

--- 'Kell'
    Kell
    "Density, Thermal Expansivity, and Compressibility of Liquid Water from
    0° to 150°C: Correlations and Tables for Atmospheric Pressure and
    Saturation Reviewed and Expressed on 1968 Temperature Scale"
    J. Chem. Eng. Data.
    (1975)
"""

from ...constants import Patm
from ..general import WaterFormula


class DensityAtm_IAPWS(WaterFormula):

    source ='IAPWS'
    temperature_unit = 'K'
    temperature_range = (253.15, 383.15)
    default = True

    def calculate(self, T):
        """Saturated liquid water density according to Patek 2009

        Input
        -----
        Temperature in K

        Output
        ------
        Density in kg/m^3

        Reference
        ---------
        Patek et al., "Reference Correlations for Thermophysical Properties of
        Liquid Water at 0.1 MPa", J. Phys. Chem. Ref. Data, 2009.
        (recommended by IAPWS)

        Notes
        -----
        - Valid between 253.15 K and 283.15 K
        """
        p0 = 0.1e6  # Pa
        R = 461.51805  # J.kg^−1.K^−1
        Tr = 10  # K
        Ta = 593  # K
        Tb = 232  # K

        alpha = Tr / (Ta - T)
        beta = Tr / (T - Tb)

        a5 = 1.93763157e-2; a6 = 6.74458446e3; a7 = -2.22521604e5; a8 = 1.00231247e8
        a9 = -1.63552118e9; a10 = 8.32299658e9; a11 = -7.5245878e-6; a12 = -1.3767418e-2
        a13 = 1.0627293e1; a14 = -2.0457795e2; a15 = 1.2037414e3

        n6 = 4; n7 = 5; n8 = 7; n9 = 8; n10 = 9
        n11 = 1; n12 = 3; n13 = 5; n14 = 6; n15 = 7

        b5 = 5.78545292e-3; b6 = -1.53195665e-2; b7 = 3.11337859e-2; b8 = -4.23546241e-2
        b9 = 3.38713507e-2; b10 = -1.19946761e-2; b11 = -3.1091470e-6; b12 = 2.8964919e-5
        b13 = -1.3112763e-4; b14 = 3.0410453e-4; b15 = -3.9034594e-4; b16 = 2.3403117e-4
        b17 = -4.8510101e-5

        m5 = 1; m6 = 2; m7 = 3; m8 = 4; m9 = 5; m10 = 6; m11 = 1
        m12 = 3; m13 = 4; m14 = 5; m15 = 6; m16 = 7; m17 = 9

        v0 = R * Tr / p0 * (a5 + a6 * alpha**n6 + a7 * alpha**n7 + a8 * alpha**n8
                            + a9 * alpha**n9 + a10 * alpha**n10 + b5 * beta**m5
                            + b6 * beta**m6 + b7 * beta**m7 + b8 * beta**m8
                            + b9 * beta**m9 + b10 * beta**m10)

        v_p0 = R * Tr / p0**2 * (a11 * alpha**n11 + a12 * alpha**n12 + a13 * alpha**n13
                                + a14 * alpha**n14 + a15 * alpha**n15 + b11 * beta**m11
                                + b12 * beta**m12 + b13 * beta**m13 + b14 * beta**m14
                                + b15 * beta**m15 + b16 * beta**m16 + b17 * beta**m17)

        v_atm = v0 + v_p0 * (Patm - p0)

        rho = 1 / v_atm

        return rho



class DensityAtm_Kell(WaterFormula):

    source ='Kell'
    temperature_unit = 'C'
    temperature_range = (0, 150)

    def calculate(self, T):
        """Ambient water density according to Kell 1975

        Input
        -----
        Temperature in C

        Output
        ------
        Density in kg/m^3

        Reference
        ---------
        - Kell : "Density, Thermal Expansivity, and Compressibility of Liquid
        Water from 0° to 150°C: Correlations and Tables for Atmospheric Pressure
        and Saturation Reviewed and Expressed on 1968 Temperature Scale",
        J. Chem. Eng. Data. 1975

        Notes
        -----
        - Used by Clegg2011
        - Valid between 0°C and 150°C
        """
        rho = 999.83952 + 16.945176 * T - 7.9870401e-3 * T**2 - 46.170461e-6 * T**3 + 105.56302e-9 * T**4 - 280.54253e-12 * T**5
        rho = rho / (1 + 16.879850e-3 * T)
        return rho


# ========================== WRAP-UP OF FORMULAS =============================

DensityAtmFormulas = (
    DensityAtm_IAPWS,
    DensityAtm_Kell,
)
