"""Various tools to calculate solution densities using Clegg formulae."""


import numpy as np

from ....constants import dissociation_numbers, Mw, molar_mass, charge_numbers
from ...water.density_atm import DensityAtm_IAPWS
from ..ionic import ionic_strength
from ..pitzer import PitzerVolumetric


Av = 1.8305  # From Archer & Wang 1990, in cm^3 kg^(1/2) mol^(-3/2)
Avx = Av * (1 / Mw) ** (1/2)  # The 1000 factor from Clegg disappears here due to Mw being in SI
rho_bold = 13  # bold rho parameter, not a density


# ----------------------------------------------------------------------------
# =================== Formulas for NaCl and Na2SO4 at 25°C ===================
# ----------------------------------------------------------------------------


params_NaCl = {
    'c1': 0.21532202E+01,  # This coefficient is WRONG in the paper's SI (indicated as E+02)
    'c2': 0,
    'c3': -0.66928951E+01,
    'c4': 0.15530704E+03,
    'c5': 0.12662763E+03,
    'c6': -0.26841488E+03,  # COEFF w**(1.75) instead of w**(2.5)
    'c7': 0,
    'c8': 0,
    'V_phi_infty': 16.62,
}

params_Na2SO4 = {
    'c1': -0.99167549E+01,
    'c2': 0.95929970E+02,
    'c3': -0.11648247E+03,
    'c4': 0.18800889E+03,
    'c5': -0.21207426E+03,
    'c6': 0,
    'c7': 0.25016809E+03,
    'c8': -0.15977556E+03,
    'V_phi_infty': 11.78,
}

params_all = {
    'NaCl': params_NaCl,
    'Na2SO4': params_Na2SO4,
}


def apparent_molar_volume_25(w, solute='NaCl'):
    """Apparent molar volume in m^3 / mol at 25°C"""

    powers = {'c1': 0.5,
              'c2': 0.75,
              'c3': 1,
              'c4': 1.5,
              'c5': 2,
              'c6': 2.5,
              'c7': 3,
              'c8': 3.5}

    params = params_all[solute]

    if solute == 'NaCl':
        powers['c6'] = 1.75

    z_m, z_x = charge_numbers[solute]
    nu_m, nu_x = dissociation_numbers[solute]
    nu_mx = nu_m + nu_x

    # Note: I use for now the 2 lines below instead of convert() because of
    # current unavailability of the convert() function [broken temporarily]
    M = molar_mass(solute)
    x = (w / M) / (w / M + (1 - w) / Mw)
    Ix = ionic_strength(solute, x=x)

    V_phi = params['V_phi_infty']
    V_phi += nu_mx * z_m * z_x * Avx / (2 * rho_bold) * np.log(1 + rho_bold * np.sqrt(Ix))

    for coeff, power in powers.items():
        V_phi += params[coeff] * w ** power

    return V_phi * 1e-6  # conversion cm^3 to m^3


def density_25(w, solute='NaCl'):
    """Density at 25°C in kg / m^3"""

    M = molar_mass(solute)

    # Note: I use for now the line below instead of convert() because of
    # current unavailability of the convert() function [broken temporarily]
    m = w / ((1 - w) * M)

    density_atm = DensityAtm_IAPWS()
    rho_w = density_atm.calculate(T=298.15)
    V_phi = apparent_molar_volume_25(w, solute=solute)

    return rho_w * (1 + m * M) / (1 + m * rho_w * V_phi)


# ----------------------------------------------------------------------------
# =================== Formula for NaCl at all temperatures ===================
# ---------------- (and for concentrations above saturation) -----------------
# ----------------------------------------------------------------------------


def q1(w):
    """First temperature coefficient for NaCl"""
    return -5.2816566e-4 - 2.443434e-5 * w


def q2(w):
    """Second temperature coefficient for NaCl"""
    return -2.421396e-6 + 2.421396e-6 * w


def density_NaCl(w, T):
    """T in Kelvins (K)"""
    Tr = 298.15
    rho = density_25(w, solute='NaCl')

    # lines below are equivalent to this version displayed in the paper:
    # rho += (T - Tr) * (q1(w) - q2(w) * Tr) * 1e3
    # rho += q2(w) / 2 * (T**2 - Tr**2) * 1e3

    rho += q1(w) * (T - Tr) * 1e3  # 1e3 for conversion g/cm^3 --> kg / m^3
    rho += q2(w) * (T - Tr)**2 / 2 * 1e3

    return rho


# ----------------------------------------------------------------------------
# ================== Formula for N2SO4 at all temperatures ===================
# ----------------------------------------------------------------------------


# High concentration ---------------------------------------------------------


def Q1(nu):
    """First temperature coefficient for Na2SO4"""
    return -5.399e-4 + 0.80541318e-3 * np.sqrt(nu) - 0.00041107238 * nu**2


def Q2(nu):
    """Second temperature coefficient for Na2SO4"""
    return -0.27716993e-8 * nu + 1.3723983e-9 * nu**4


def density_Na2SO4_high_conc(w, T):
    """Valid above weight fraction of 22%. T in Kelvins (K)"""
    Tr = 298.15
    rho = density_25(w, solute='Na2SO4')

    nu = (1 - w) / 0.78

    rho += Q1(nu) * (T - Tr) * 1e3
    rho += Q2(nu) * (T**3 - Tr**3) * 1e3

    return rho


# Low concentration ----------------------------------------------------------
# NOTE -- There seems to be a problem with the low-concentration formulas
# below, because the values for the apparent molar volumes and densities
# do not match the tables from the Supplemental Information in Clegg's paper.
# (also, it is supposed to have a continuity with the high-concentration
# formulas at w=0.22 -- the "reference concentratinon" and it is not the case)


beta0_coeffs = 0.0024497654, 0, -0.48224610e-3, 0.11372104e-5
beta1_coeffs = -1.0086131, 28.944503, 0.17371696, -0.26199156e-3
C0_coeffs = 0.59267496e-5, -0.0022005223, 0, 0
alpha = 1.4
Ratm = 82.05746  # idel gas constants when atm is used instead of MPa


def v_phi_infty(T):
    """Apparent molar volume at infinite dilution (T in K)"""
    return 28746.8530 + 6.802415 * T - 4886.246974 * np.log(T) - 8.715969e5 / T


def _calculate_parameter(T, *coeffs):
    """Temperature correlations for parameters beta0, beta1, C0.

    T in K
    """
    c0, c1, c2, c3 = coeffs
    return c0 + c1 / T + c2 * np.log(T) + c3 * T

def density_Na2SO4_low_conc(m, T):
    """Density at 25°C in kg / m^3. T in Kelvins (K)"""
    beta0 = _calculate_parameter(T, *beta0_coeffs)
    beta1 = _calculate_parameter(T, *beta1_coeffs)
    Cv = _calculate_parameter(T, *C0_coeffs)
    v0 = v_phi_infty(T)

    pitz = PitzerVolumetric(
        solute='Na2SO4',
        T=T,
        R=Ratm,
        A_v=Av,
        C_v=Cv,
        v_0=v0,
        beta0=beta0,
        beta1=beta1,
        alpha1=alpha,
    )

    v_phi = pitz.apparent_molar_volume(m=m) * 1e-6  # conversion cm^3 --> m^3

    Ms = molar_mass('Na2SO4')

    density_atm = DensityAtm_IAPWS()
    rho_w = density_atm.calculate(T)

    return rho_w * (1 + m * Ms) / (1 + m * rho_w * v_phi)
