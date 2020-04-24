"""Functions to calculate the vapor pressure of water as a function of
temperature using NIST or IAPWS recommended equations.

Sources
-------

- Wexler and Greenspan : "Vapor Pressure Equation for Water in the Range 0 to
100°C" (1971). Valid from 0 to 100°C. We use Equation (17) and not the
simplified Equations 18a-c.

- Bridgeman and Aldrich : "Vapor Pressure Tables for Water" (1964).
Valid from 0 to 374.15°C. Use 'Bridgeman'.

- Wagner and Pruß : "The IAPWS Formulation 1995 for the Thermodynamic Properties
of Ordinary Water Substance for General and Scientific Use" (2002).
Temperature validity range seems to be 0 - 1000°C.
Equation is (2.5) page 398.

Notes
-----
Some older references use different scales of temperatures (e.g. IPS68 / 90)
which might be why some values for the critical point are slightly different.
Here we consider all absolute temperatures as being in Kelvin.
"""

# TODO: Clarify which equations are recommended by IAPWS and which one should be default.
# TODO: Switch automatically to another equation if outside of range.


from numpy import log, exp, arccosh, sqrt

from ...constants import Tc


# General Info about the formulas
sources = ['Wexler', 'Bridgeman', 'Wagner']

default_source = 'Wagner'

temperature_units = {'Wexler': 'K',
                     'Bridgeman': 'C',
                     'Wagner': 'K'}

temperature_ranges = {'Wexler': (273.15, 373.15),
                      'Bridgeman': (0, 374.15),
                      'Wagner': (273.15, Tc)}  # in fact 273.16 (triple point)


def psat_wexler(T):
    """Water Saturation pressure according to Wexler 1971, eq. (17). T in K."""

    E = [-7.51152e3, 9.65389644e1, 2.399897e-2,
         -1.1654551e-5, -1.2810336e-8, 2.0998405e-11]

    B = -1.2150799e1

    lnp = B * log(T)
    for i, e in enumerate(E):
        lnp += e * T**(i - 1)

    return exp(lnp)


def psat_bridgeman(T):
    """Water Saturation pressure according to Bridgeman 1964. T in C."""

    A = 1.06423320; B = 1.0137921; C = 5.83531e-4; D = 4.16385282;
    E = 237.098157; F = 0.30231574; G = 3.377565e-3; H = 1.152894;
    K = 0.745794; L = 654.2906; M = 266.778

    Y1 = D * (T - 187) / (T + E)
    X = 0.01 * (T - 187)
    Z = -1.87 + 3.74 * (H - K * arccosh(L / (T + M)))
    a = Z**2 * (1.87**2 - Z**2) / (F * (1 + G * T))

    Y2 = 3 * sqrt(3) / (2 * 1.87**3) * (X - 0.01 * a) * (1.87**2 - (X - 0.01 * a)**2) / 100

    logp = A + Y1 - B * (1 + C * T) * Y2

    return (10**logp) * 101325


def psat_wagner(T):
    """Water saturation pressure according to Wagner & Pruß, T in K."""

    Pc = 22.064e6; Tc = 647.096; v = 1 - T / Tc
    ais = -7.85951783, 1.84408259, -11.7866497, 22.6807411, -15.9618719, 1.80122502
    a1, a2, a3, a4, a5, a6 = ais

    val = Tc / T * (a1 * v + a2 * v**1.5 + a3 * v**3 + a4 * v**3.5 + a5 * v**4 + a6 * v**7.5)

    p = exp(val) * Pc

    return p


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Wexler': psat_wexler,
            'Bridgeman': psat_bridgeman,
            'Wagner': psat_wagner}

