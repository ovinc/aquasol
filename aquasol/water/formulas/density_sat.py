"""Function to calculate the desnity of ambient water as a function of
temperature using IAPWS recommended equation.

Sources
-------

- Wagner and Pruß : "The IAPWS Formulation 1995 for the Thermodynamic
Properties of Ordinary Water Substance for General and Scientific Use" (2002).
Equation 2.6 page 399

- Conde, M. R., Properties of aqueous solutions of lithium and calcium
chlorides: formulations for use in air conditioning equipment design.
International Journal of Thermal Sciences 43, 367–382 (2004).

"""

from ...constants import Tc, rhoc


# General Info about the formulas

default_source = 'Wagner'

temperature_units = {'Wagner': 'K',
                     'Conde': 'K'}

temperature_ranges = {'Wagner': (273.15, Tc),
                      'Conde': (273.15, Tc)}


def density_wagner(T):
    """Saturated water density according to Wagner and Pruss 2002 (IAPWS 95)

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


def density_conde(T):
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
    International Journal of Thermal Sciences 43, 367–382 (2004).

    """
    c1 = 1.9937718430; c2 = 1.0985211604; c3 = -0.5094492996
    c4 = -1.7619124270; c5 = -44.9005480267; c6 = -723692.2618632
    phi = 1 - T / Tc
    rho = rhoc * (1 + c1 * phi**(1/3) + c2 * phi**(2/3) + c3 * phi**(5/3)
                    + c4 * phi**(16/3) + c5 * phi**(43/3) + c6 * phi**(110/3))
    return rho


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Wagner': density_wagner,
            'Conde': density_conde}

sources = [source for source in formulas]
