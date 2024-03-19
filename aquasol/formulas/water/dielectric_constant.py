"""Function to calculate the dielectric constant of water.

Sources
-------

--- 'Archer'
    Archer, D. G. & Wang, P.
    The Dielectric Constant of Water and Debye-Hückel Limiting Law Slopes.
    Journal of Physical and Chemical Reference Data 19, 371-411
    (1990)

Also used is this formula for water density, required in Archer:
--- 'IAPWS'
    Patek et al.
    "Reference Correlations for Thermophysical Properties of Liquid Water
    at 0.1 MPa"
    J. Phys. Chem. Ref. Data
    (2009)
"""

import numpy as np
import matplotlib.pyplot as plt
from pynverse import inversefunc

from ...format import make_array_method
from ...constants import Patm
from ..general import WaterFormula
from ..water.density_atm import DensityAtm_IAPWS


rho = DensityAtm_IAPWS()

# I copied all constants from Archer and Wang in case of changes in definitions

# Note: here calculated at Patm, but equation valid for other pressures

alpha = 18.1458392e-30
mu = 6.1375776e-30
Na = 6.0221367e23
k = 1.380658e-23
Mw = 0.0180153
epsilon0 = 8.8541878e-12

b_coeffs = (
    -4.044525e-2,
    103.6180,
    75.32165,
    -23.23778,
    -3.548184,
    - 1246.311,
    263307.7,
    -6.928953e-1,
    -204.4473,
)

T1 = 215
rho_0 = 1000
patm_MPa = Patm / 1e6


def molar_volume(T):
    return Mw / rho.calculate(T=T)


def g_minus_one_over_rho(T, p):
    b1, b2, b3, b4, b5, b6, b7, b8, b9 = b_coeffs
    result = (
        b1 * p / T +
        b2 * T**(-1/2) +
        b3 * (T - T1)**(-1) +
        b4 * (T - T1)**(-1/2) +
        b5 * (T - T1)**(-1/4) +
        np.exp(b6 / T + b7 / T**2 + b8 * p / T + b9 * p / T**2)
    )
    return result


def g(T):
    return 1 + g_minus_one_over_rho(T, p=patm_MPa) * rho.calculate(T=T) / rho_0


def f(T):
    return Na / (3 * molar_volume(T)) * (alpha + g(T) * mu**2 / (3 * epsilon0 * k * T))


def e(epsilon):
    return (epsilon - 1) * (2 * epsilon + 1) / (9 * epsilon)


class DielectricConstant_Archer(WaterFormula):

    source ='IAPWS'
    temperature_unit = 'K'
    # Validity for Archer is muchwider, but the final result is limited by
    # the density formula used (here IAPWS)
    temperature_range = rho.temperature_range
    default = True

    @make_array_method
    def calculate(self, T):
        """Dielectric constant of water according to Archer and Wang (1990)

        Input
        -----
        Temperature in K

        Output
        ------
        Dielectric constant [-]
        """
        f_calc = f(T)
        epsilon_approx = 9 / 2 * f_calc
        epsilon_calc = inversefunc(e, domain=(0.9 * epsilon_approx, 1.1 * epsilon_approx))
        return epsilon_calc(f_calc)


# ========================== WRAP-UP OF FORMULAS =============================

DielectricConstantFormulas = (
    DielectricConstant_Archer,
)
