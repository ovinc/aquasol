"""Function to calculate the desnity of ambient water as a function of
temperature using IAPWS recommended equation.

Sources
-------

- Kell : "Density, Thermal Expansivity, and Compressibility of Liquid
Water from 0° to 150°C: Correlations and Tables for
Atmospheric Pressure and Saturation Reviewed and
Expressed on 1968 Temperature Scale", 1975
"""

from numpy import log, exp, arccosh, sqrt

from ...constants import Tc


# General Info about the formulas

default_source = 'Kell'

temperature_units = {'Kell': 'C'
                     }

temperature_ranges = {'Kell': (0, 150)}


def density_kell(T):
    """Ambient water density according to Kell 1975

    Input
    -----
    Temperature in C

    Output
    ------
    Density in kg/m^3

    Reference
    ---------
    Kell : "Density, Thermal Expansivity, and Compressibility of Liquid
    Water from 0° to 150°C: Correlations and Tables for
    Atmospheric Pressure and Saturation Reviewed and
    Expressed on 1968 Temperature Scale", 1975, equations (12) and (16)

    Notes
    -----
    - Used by Clegg2011
    - Valid between 0°C and 150°C
    """

    a0, a1, a2  = 999.83952, 16.945176, -7.9870401e-3
    a3, a4, a5  = -46.170461e-6, 105.56302e-9, -280.54253e-12
    b = 16.879850e-3

    rho = (a0 + a1*T + a2*T**2 + a3*T**3 + a4*T**4 + a5*T**5) / (1 + b*T)

    return rho


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Kell': density_kell}

sources = [source for source in formulas]
