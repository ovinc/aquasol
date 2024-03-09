"""Al Ghafri formulae for various salts

Sources
-------
- Al Ghafri et al., Densities of Aqueous MgCl2(aq), CaCl2 (aq), KI(aq),
NaCl(aq), KCl(aq), AlCl3(aq), and (0.964 NaCl + 0.136 KCl)(aq) at
Temperatures Between (283 and 472) K, Pressures up to 68.5 MPa, and
Molalities up to 6 mol·kg -1.
Journal of Chemical & Engineering Data 57, 1288-1304 (2012).
"""

import numpy as np

from ....constants import Tc, Patm
from ...general import SolutionFormula
from ...water.vapor_pressure import VaporPressure_IAPWS
from ...water.density_sat import DensitySat_IAPWS


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
    vapor_pressure = VaporPressure_IAPWS()
    p_ref = vapor_pressure.calculate(T)

    density_sat = DensitySat_IAPWS()
    rho_sat = density_sat.calculate(T)

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


# ===================== Coefficients for different salts =====================

def coeffs_CaCl2():

    a = np.zeros((4, 5))
    a[1, :] = [2546.760, -39884.946, 102056.957, -98403.334, 33976.048]
    a[2, :] = [-1362.157, 22785.572, -59216.108, 57894.824, -20222.898]
    a[3, :] = [217.778, -3770.645, 9908.135, -9793.484, 3455.587]

    b = np.zeros((2, 4))
    b[0, :] = [-1622.4, 9383.8, -14893.8, 7309.10]
    b[1, :] = [307.24, -1259.10, 2034.03, -1084.94]

    c = np.zeros(3)
    c[:] = [0.11725, -0.00493, 0.00231]

    return a, b, c


def coeffs_KCl():

    a = np.zeros((4, 5))
    a[1, :] = [2332.802, -39637.418, 104801.288, -104266.828, 37030.556]
    a[2, :] = [-1287.572, 23543.994, -63846.097, 65023.561, -23586.370]
    a[3, :] = [206.032, -4003.757, 11128.162, -11595.475, 4295.498]

    b = np.zeros((2, 4))
    b[0, :] = [-1622.4, 9383.8, -14893.8, 7309.10]
    b[1, :] = [211.49, -888.16, 1400.09, -732.79]

    c = np.zeros(3)
    c[:] = [0.11725, -0.00170, 0.00083]

    return a, b, c


def coeffs_KI():

    a = np.zeros((4, 5))
    a[1, :] = [8657.149, -94956.477, 167497.772, -74952.063, -8734.207]
    a[2, :] = [-14420.621, 137360.624, -184940.639, -11953.289, 79847.960]
    a[3, :] = [7340.083, -66939.345, 81446.737, 23983.386, -49031.473]

    b = np.zeros((2, 4))
    b[0, :] = [-1622.4, 9383.8, -14893.8, 7309.10]
    b[1, :] = [241.84, -1030.61, 1548.15, -754.36]

    c = np.zeros(3)
    c[:] = [0.11725, -0.01026, 0.00842]

    return a, b, c


def coeffs_MgCl2():

    a = np.zeros((4, 5))
    a[1, :] = [2385.823, -38428.112, 99526.269, -97041.399, 33841.139]
    a[2, :] = [-1254.938, 21606.295, -56988.274, 56465.943, -19934.064]
    a[3, :] = [192.534, -3480.374, 9345.908, -9408.904, 3364.018]

    b = np.zeros((2, 4))
    b[0, :] = [-1622.4, 9383.8, -14893.8, 7309.10]
    b[1, :] = [358.00, -1597.10, 2609.47, -1383.91]

    c = np.zeros(3)
    c[:] = [0.11725, -0.00789, 0.00142]

    return a, b, c


def coeffs_NaCl():

    a = np.zeros((4, 5))
    a[1, :] = [2863.158, -46844.356, 120760.118, -116867.722, 40285.426]
    a[2, :] = [-2000.028, 34013.518, -88557.123, 86351.784, -29910.216]
    a[3, :] = [413.046, -7125.857, 18640.780, -18244.074, 6335.275]

    b = np.zeros((2, 4))
    b[0, :] = [-1622.4, 9383.8, -14893.8, 7309.10]
    b[1, :] = [241.57, -980.97, 1482.31, -750.98]

    c = np.zeros(3)
    c[:] = [0.11725, -0.00134, 0.00056]

    return a, b, c


# ================== Base class for all al ghafri formulas ===================


class Density_AlGhafri_Base(SolutionFormula):
    """Gathers all info common to all Al Ghafri Formulae"""

    source ='Al Ghafri'

    temperature_unit = 'K'
    temperature_range = (283.15, 473.15)

    concentration_unit = 'm'

    with_water_reference = True

    def calculate(self, m, T):
        rho = rho_alghafri(m, T, Patm, *self.coeffs)
        rho0 = rho_alghafri(0, T, Patm, *self.coeffs)
        return rho0, rho


# ============================ Specific formulas =============================


class Density_CaCl2_AlGhafri_Base(Density_AlGhafri_Base):
    solute = 'CaCl2'
    concentration_range = (0, 6)
    coeffs = coeffs_CaCl2()


class Density_KCl_AlGhafri_Base(Density_AlGhafri_Base):
    solute = 'KCl'
    concentration_range = (0, 4.5)
    coeffs = coeffs_KCl()


class Density_KI_AlGhafri_Base(Density_AlGhafri_Base):
    solute = 'KI'
    concentration_range = (0, 1.05)
    coeffs = coeffs_KI()


class Density_MgCl2_AlGhafri_Base(Density_AlGhafri_Base):
    solute = 'MgCl2'
    concentration_range = (0, 5)
    coeffs = coeffs_MgCl2()


class Density_NaCl_AlGhafri_Base(Density_AlGhafri_Base):
    solute = 'NaCl'
    concentration_range = (0, 6)
    coeffs = coeffs_NaCl()