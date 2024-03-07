"""Functions for the calculation of the density of solutions."""

import numpy as np

from ....constants import Tc, molar_mass
from ...water.vapor_pressure import VaporPressure_Wagner
from ...water.density_sat import DensitySat_Wagner
from ...water.density_atm import DensityAtm_Patek

from ..pitzer import PitzerVolumetric


# ----------------------------------------------------------------------------
# ============================ Pitzer-based formulas =========================
# ----------------------------------------------------------------------------


# ============= Molar volume Constants from Krumgalz 1996 (25°C) =============
# ----------- Note: MANY more solutes available in that reference ------------

Av_krum = 1.875

vm0_infty_krum = {
    'NaCl': 16.620,  # cm^3 / mol
    'KCl': 26.848,
    'LiCl': 16.866,
    'CaCl2': 17.612,
    'LiBr': 23.758,
    'KI': 45.151,
    'NaBr': 23.479,
    'Na2SO4': 11.766,
    'MgCl2': 14.083,
}

# Converted to kg·mol–1·MPa–1 (originally bar-1)
params_krum = {  # beta0    beta1       C
    'NaCl': (1.2335e-4, 0.43543e-4, -0.6578e-5),
    'KCl': (1.2793e-4, 0.8948e-4, -0.7131e-5),
    'LiCl': (0.3853e-4, 1.5553e-4,  -0.1541e-5),
    'CaCl2': (1.3107e-4, -2.4575e-4,  -0.1265e-5),
    'LiBr': (0.2399e-4, 0.2406e-4,  -0.1744e-5),
    'KI': (0.5398e-4, 1.4438e-4, -0.2479e-5),
    'NaBr': (0.7607e-4, 0.9525e-4, -0.3491e-5),
    'Na2SO4': (5.3250e-4, 12.932e-4, -2.914e-5),
    'MgCl2': (1.6933e-4, -5.2068e-4, -0.5698e-5),
}

# max molalities (mol/kg) for formula to be valid (cf table 2)
m_max_krum = {
    'NaCl': 6.1,
    'KCl': 4.7,
    'LiCl': 19.6,
    'CaCl2': 7.7,
    'LiBr': 17.7,
    'KI': 8.6,
    'NaBr': 8.0,
    'Na2SO4': 1.5,
    'MgCl2': 5.8,
}

# ============= Molar volume Constants from Steiger 2022 (25°C) ==============

# Slightly different from original Krumgalz (1.875, cf p. 665), taken from Archer and Wang
Av_steiger = 1.8305
vm0_infty_steiger = {'NaCl': 16.620}
params_steiger = {'NaCl': (1.17996e-4, 0.713188e-4, -0.586951e-5)}

# ================= Gather coeffs from Steiger and Krumgalz =================

Avs = {'Krumgalz': Av_krum, 'Steiger': Av_steiger}
vm0_inftys = {'Krumgalz': vm0_infty_krum, 'Steiger': vm0_infty_steiger}
params = {'Krumgalz': params_krum, 'Steiger': params_steiger}


def apparent_molar_volume_pitzer(m, solute='NaCl', source='Krumgalz'):
    """Determine apparente molar volume from Krumgaltz."""
    beta0, beta1, Cv = params[source][solute]
    v0 = vm0_inftys[source][solute]
    pitzer_v = PitzerVolumetric(T=298.15,
                                solute=solute,
                                A_v=Avs[source],
                                beta0=beta0,
                                beta1=beta1,
                                C_v=Cv,
                                v_0=v0)

    # conversion cm^3 / mol --> m^3 / mol
    return pitzer_v.apparent_molar_volume(m=m) * 1e-6


def density_pitzer(m, solute='NaCl', source='Krumgalz'):
    """Density at 25°C in kg / m^3"""
    v_phi = apparent_molar_volume_pitzer(m, solute=solute, source=source)
    Ms = molar_mass(solute)
    density_atm = DensityAtm_Patek()
    rho_w = density_atm.calculate(T=298.15)
    return rho_w, rho_w * (1 + m * Ms) / (1 + m * rho_w * v_phi)


# ----------------------------------------------------------------------------
# ============================== Other formulas ==============================
# ----------------------------------------------------------------------------


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
    vapor_pressure = VaporPressure_Wagner()
    p_ref = vapor_pressure.calculate(T)

    density_sat = DensitySat_Wagner()
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
