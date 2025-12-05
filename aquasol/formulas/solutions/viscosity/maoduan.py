"""Viscosity of salt solutions, from Mao and Duan.

Reference
---------
Mao, S. & Duan, Z.
The Viscosity of Aqueous Alkali-Chloride Solutions up to 623 K, 1,000 bar,
and High Ionic Strength.
Int J Thermophys 30, 1510-1523 (2009).
"""

import numpy as np

from ...general import SolutionFormula
from ...water.density_atm import DensityAtm_IAPWS


# Parameters for A, B, C polynomials (Eqs. 3–5)

PARAMS = {
    "LiCl": {
        "a": np.array([0.62204136e-2, 0.54436974e-3, -0.40443190e-6]),
        "b": np.array([0.14987325e-1, -0.66617390e-4, 0.52113332e-7]),
        "c": np.array([0.12101624e-5, 0.17772678e-6]),
    },
    "NaCl": {
        "a": np.array([-0.21319213, 0.13651589e-2, -0.12191756e-5]),
        "b": np.array([0.69161945e-1, -0.27292263e-3, 0.20852448e-6]),
        "c": np.array([-0.25988855e-2, 0.77989227e-5]),
    },
    "KCl": {
        "a": np.array([-0.42122934, 0.18286059e-2, -0.13603098e-5]),
        "b": np.array([0.11380205e-1, 0.47541391e-5, -0.99280575e-7]),
        "c": np.array([0.0, 0.0]),  # C = 0 for KCl
    },
}

density_H2O = DensityAtm_IAPWS()

# Water viscosity model coefficients (Eq. 6)
d = np.array(
    [
        0.28853170e7,
        -0.11072577e5,
        -0.90834095e1,
        0.30925651e-1,
        -0.27407100e-4,
        -0.19283851e7,
        0.56216046e4,
        0.13827250e2,
        -0.47609523e-1,
        0.35545041e-4,
    ]
)


def ln_viscosity_H2O(T):
    """Compute ln(eta_H2O) based on Eq. 6."""
    rho = density_H2O.calculate(T) / 1000  # grams per cm^3
    T_powers = T ** np.arange(-2, 3)  # T^-2 to T^2
    T_rho_powers = rho * T ** np.arange(-2, 3)  # ρ*T^-2 to ρ*T^2
    return np.dot(d[:5], T_powers) + np.dot(d[5:], T_rho_powers)


def compute_polynomial_coeffs(T, solute):
    """Compute A, B, C coefficients as functions of temperature."""
    T_vec = np.array([1, T, T**2])
    A = np.dot(PARAMS[solute]["a"], T_vec)
    B = np.dot(PARAMS[solute]["b"], T_vec)
    C = np.dot(PARAMS[solute]["c"], T_vec[:2])  # Only c0 + c1*T
    return A, B, C


def viscosity_solution(m, T, coeffs):
    """
    Compute dynamic viscosity eta in Pa·s for given
    - m (mol/kg)
    - T (K),
    - coeffs: A, B, C
    """
    ln_eta_H2O = ln_viscosity_H2O(T)
    eta_H2O = np.exp(ln_eta_H2O)

    A, B, C = coeffs
    ln_eta_r = A * m + B * m**2 + C * m**3
    eta_r = np.exp(ln_eta_r)

    return eta_H2O, eta_r * eta_H2O  # in Pa·s


class Viscosity_MaoDuan_Base(SolutionFormula):

    source = 'Mao&Duan'

    temperature_unit = 'K'
    temperature_range = (273, 623)

    concentration_unit = 'm'
    concentration_range = None  # DEFINE IN SUBCLASSES

    with_water_reference = True

    def calculate(self, m, T):
        """Viscosity calculated from Mao&Duan, m (mol/kg) T (K)."""
        coeffs = compute_polynomial_coeffs(T=T, solute=self.solute)
        return viscosity_solution(m, T, coeffs=coeffs)


class Viscosity_MaoDuan_NaCl_Base(Viscosity_MaoDuan_Base):
    solute = 'NaCl'
    concentration_range = (0, 6)


class Viscosity_MaoDuan_LiCl_Base(Viscosity_MaoDuan_Base):
    solute = 'LiCl'
    concentration_range = (0, 16.7)


class Viscosity_MaoDuan_KCl_Base(Viscosity_MaoDuan_Base):
    solute = 'KCl'
    concentration_range = (0, 4.5)
