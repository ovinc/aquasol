"""Functions for the calculation of the density of solutions."""

import numpy as np

from ....constants import Tc
from ....water import vapor_pressure
from ....water import density_sat


def rho_alghafri(m, T, P, a, b, c):
    """General formula for density accorging to Al Ghafri 2012.

    Valid for many solutes including NaCl, KCl, CaCl2, etc.

    Inputs
    ------
    m: molality of salt
    T: temperature in K
    a: list of coefficients alpha from table 10
    b: list of coefficients beta from table 9 and 10
    c: list of coefficients gamma from table 9 and 10

    Outputs
    -------
    Density of solution, kg/m^3

    Reference
    ---------
    Al Ghafri et al., Densities of Aqueous MgCl 2 (aq), CaCl 2 (aq), KI(aq),
    NaCl(aq), KCl(aq), AlCl 3 (aq), and (0.964 NaCl + 0.136 KCl)(aq) at
    Temperatures Between (283 and 472) K, Pressures up to 68.5 MPa, and
    Molalities up to 6 mol·kg-1.
    Journal of Chemical & Engineering Data 57, 1288-1304 (2012).

    Notes
    -----
    (from the article's last page)
    These are valid in the temperature range (298.15 to 473.15) K and at
    pressures up to 68.5 MPa for all brines studied except in the case of
    AlCl3 (aq) where the temperature is restricted to the range (298.15 to
    373.15) K. The correlations are valid for all molalities up to
    (5.0,      6.0,       1.06,   6.0,      4.5,     2.0,      and 4.95) mol·kg-1 for
    MgCl2(aq), CaCl2(aq), KI(aq), NaCl(aq), KCl(aq), AlCl3(aq),
    and (0.864 NaCl + 0.136 KCl)(aq), respectively.
    """

    p_ref = vapor_pressure(T, 'K', source='Wagner')
    rho_sat = density_sat(T, 'K', source='Wagner')

    # reference density (solution density at reference pressure p_ref(T), which
    # is taken to be the vapor pressure of pure water at the given temperature.

    rho_ref = rho_sat

    for i in range(1, 4):
        rho_ref += a[i][0] * m**((i + 1) / 2)  # eq 9

    for i in range(1, 4):
        for j in range(1, 5):
            rho_ref += a[i][j] * m**((i + 1) / 2) * (T / Tc)**((j + 1) / 2)

    # Parameters of the Tammann-Tait equation --------------------------------

    B = 0
    for i in range(2):
        for j in range(4):
            B += b[i][j] * m**i * (T / Tc)**j  # eq10
    B *= 1e6

    C = c[0] + c[1] * m + c[2] * m**(3 / 2)  # eq 11

    # Final calculation ------------------------------------------------------

    rho = rho_ref * (1 - C * np.log((B + P) / (B + p_ref)))**(-1)  # eq 7

    return rho


def relative_rho_conde(z, coeffs):
    """Relative Density of LiCl and CaCl2 according to Conde 2004.

    - z is mass fraction (w / (1 - w))
    - T is temperature in K
    - coeffs are the rho_i coefficients of table 4
    """

    d = 0
    for i, c in enumerate(coeffs):
        d += c * z**i

    return d


def rho_tang(w, coeffs):
    """From Tang 1996, only at 25°C"""
    w = w * 100
    rho0 = 997.1  # density of pure water (at 25°C)
    rho = rho0
    for i, coeff in enumerate(coeffs):
        rho += coeff * w ** (i + 1)
    return rho0, rho
