"""Function to calculate the desnity of ambient water as a function of
temperature using IAPWS recommended equation.

Sources
-------

- Wagner and Pruß : "The IAPWS Formulation 1995 for the Thermodynamic Properties
of Ordinary Water Substance for General and Scientific Use" (2002).
Equation 2.6 page 399
"""

from numpy import log, exp, arccosh, sqrt

from ...constants import Tc, rhoc


# General Info about the formulas

default_source = 'Wagner'

temperature_units = {'Wagner': 'K'
                     }

temperature_ranges = {'Wagner': (273.15, Tc)}


def density_wagner(T):
    """Saturated water density according to Wagner and Pruss 1995 (IAPWS)

    Input
    -----
    Temperature in C

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
    c1 = 1.99274064; c2 = 1.09965342; c3 = -0.510839303
    c4 = -1.75493479; c5 = -45.5170352; c6 = -6.74694450e5
    phi = 1 - T / Tc
    rho = rhoc * (1 + c1 * phi**(1/3) + c2 * phi**(2/3) + c3 * phi**(5/3)
                    + c4 * phi**(16/3) + c5 * phi**(43/3) + c6 * phi**(110/3))
    return rho


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Wagner': density_wagner}

sources = [source for source in formulas]
