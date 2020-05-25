"""Functions for the calculation of the density of solutions."""

import numpy as np
import itertools

from thermov.constants import Tc, Pc, rhoc
from thermov.water import vapor_pressure
from thermov.water import density_sat


def main():
    """Calculates Al Ghafri for NaCl, as an example."""

    a = np.zeros((4, 5))

    a[1][0] = 2863.158; a[1][1] = -46844.356; a[1][2] = 120760.118
    a[1][3] = -116867.722; a[1][4] = 40285.426

    a[2][0] = -2000.028; a[2][1] = 34013.518; a[2][2] = -88557.123;
    a[2][3] = 86351.784; a[2][4] = -29910.216

    a[3][0] = 413.046; a[3][1] = -7125.857; a[3][2] = 18640.780;
    a[3][3] = -18244.074; a[3][4] = 6335.275

    b = np.zeros((2, 4))
    b[0][0] = -1622.4; b[0][1] = 9383.8; b[0][2] = -14893.8; b[0][3] = 7309.10
    b[1][0] = 241.57; b[1][1] = -980.97; b[1][2] = 1482.31; b[1][3] = -750.98

    c = np.zeros(3)
    c[0] = 0.11725; c[1] = -0.00134; c[2] = 0.00056

    rho = rho_al_ghafri(6, 298.15, 1e5, a, b, c)
    print(rho)


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
    Molalities up to 6 mol·kg −1.
    Journal of Chemical & Engineering Data 57, 1288-1304 (2012).

    Notes
    -----
    (from the article's last page)
    These are valid in the temperature range (298.15 to 473.15) K and at
    pressures up to 68.5 MPa for all brines studied except in the case of
    AlCl3 (aq) where the temperature is restricted to the range (298.15 to
    373.15) K. The correlations are valid for all molalities up to
    (5.0,      6.0,       1.06,   6.0,      4.5,     2.0,      and 4.95) mol·kg−1 for
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


if __name__ == '__main__':
    main()
