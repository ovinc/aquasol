"""Implementation of Pitzer equations (activity, volumetric).

Mostly based on Michael Steiger's group papers.
"""

import numpy as np

from ...constants import R as ideal_gas_constant
from ...constants import Mw, charge_numbers, dissociation_numbers
from .ionic import ionic_strength


b = 1.2  # kg^1/2.mol^-1/2


class PitzerBase:
    """Base class for Pitzer equations for water & solute activity, or volumetric."""

    def __init__(self, T=298.15, solute='NaCl', R=None, **coeffs):
        """Init PitzerBase object.

        Input
        -----
        T: temperature in K
        solute: solute name (str, default 'NaCl')
        R: (optional) replacement value for the ideal gas constant, R
           (useful if e.g. units use atmospheres instead of MPa etc.)
        coeffs: Pitzer coefficients
        """
        self.T = T
        self.R = R if R is not None else ideal_gas_constant
        self.solute = solute

        for coeff_name, coeff_value in coeffs.items():
            setattr(self, coeff_name, coeff_value)

        self.z_m, self.z_x = charge_numbers[solute]
        self.nu_m, self.nu_x = dissociation_numbers[solute]
        self.nu_mx = self.nu_m + self.nu_x

    @staticmethod
    def g(x):
        """Function used to calculate the second virial coefficients"""
        y = 2 * (1 - (1 + x) * np.exp(-x))
        # Below is a trick to avoid the problem of division by zero, since g(0) = 0
        return np.divide(y, x**2, out=np.ones_like(x), where=x != 0)

    def virial_B(self, m, func=None):
        """Calculate second virial coefficient at a given molality

        Input
        -----
        - m: molality in mol/kg
        - func: which function used with beta1 / beta2 (default: g(x))

        Output
        ------
        Second Virial coefficients in units corresponding to input coeffs.
        """
        func = self.g if func is None else func
        sqrtI = ionic_strength(self.solute, m=m)**(1 / 2)
        x1 = self.alpha1 * sqrtI
        x2 = self.alpha2 * sqrtI
        return self.beta0 + self.beta1 * func(x1) + self.beta2 * func(x2)


class PitzerVolumetric(PitzerBase):
    """Implementation of Pitzer Equations for volumetric properties"""

    def __init__(self, T=298.15, solute='NaCl', R=None, **coeffs):
        """Init PitzerVolumertic object.

        Input
        -----
        T: temperature in K
        solute: solute name (str, default 'NaCl')
        R: (optional) replacement value for the ideal gas constant, R
           (useful if e.g. units use atmospheres instead of MPa etc.)
        coeffs: must contain the following keys:
        - A_v [cm3·kg1/2·mol-3/2]: first virial coefficient
        - beta0, beta1 [kg·mol-1·MPa-1]: second virial coefficient parameters
        - C_v [kg2·mol-2·MPa-1]: third virial coefficient
        - v_0 [cm3/mol]: apparent molar volume at infinite dilution

        optional keys (to specify if electrolyte is 2:2)
        - beta2 (default 0)
        - alpha1 [kg1/2mol-1/2] (default 2)
        - alpha2 [kg1/2mol-1/2] (default 0)

        NOTE: the beta coefficients are in [kg·mol-1·MPa-1]
        CAUTION: non-SI unit (makes output of molar volumes in cm^3 / mol)

        NOTE: second Virial coefficients Bv are in [kg·mol-1·MPa-1].
        """
        coeffs['beta2'] = coeffs.get('beta2', 0)    # add default values
        coeffs['alpha1'] = coeffs.get('alpha1', 2)  # (these alpha values do not work for 2:2 electrolytes)
        coeffs['alpha2'] = coeffs.get('alpha2', 0)
        super().__init__(T=T, solute=solute, R=R, **coeffs)

    def apparent_molar_volume(self, m):
        """Apparent molar volume in cm^3 / mol at given molality

         Input
        -----
        - m: molality in mol/kg

        Output
        ------
        Apparent molar volume in cm^3 / mol (NON-SI)
        """
        Av = self.A_v
        Bv = self.virial_B(m=m)
        Cv = self.C_v
        T = self.T
        R = self.R

        sqrtI = ionic_strength(self.solute, m=m)**(1 / 2)

        v0 = self.v_0
        v1 = self.nu_mx * self.z_m * self.z_x * Av / (2 * b) * np.log(1 + b * sqrtI)
        v2 = 2 * R * T * self.nu_m * self.nu_x * (Bv * m + (self.nu_m * self.z_m * Cv) * m**2)

        return v0 + v1 + v2


class PitzerActivity(PitzerBase):
    """Implementation of Pitzer equations for activity (phi / gamma)"""

    def __init__(self, T=298.15, solute='NaCl', **coeffs):
        """Init PitzerActivity object.

        Input
        -----
        T: temperature in K
        solute: solute name (str, default 'NaCl')
        coeffs: must contain the following keys:
        - A_phi: first virial coefficient
        - alpha1, alpha2, beta0, beta1, beta2: 2d virial coefficient parameters
        - C_phi: third virial coefficient
        """
        super().__init__(T=T, solute=solute, **coeffs)
        self.C_gamma = 3 / 2 * self.C_phi

    def _activity_coeff(self, m, f, B, C):
        """Generic calculation for both osmotic coeff and ln(gamma).

        Input:
        m: molality
        f: Debye factor (f_phi or f_gamma)
        B, C: second and third virial coefficients
        """
        p1 = self.z_m * self.z_x * f
        p2 = B * 2 * m * (self.nu_m * self.nu_x) / self.nu_mx
        p3 = C * 2 * m**2 * (self.nu_m * self.nu_x)**(3 / 2) / self.nu_mx
        return p1 + p2 + p3

    @staticmethod
    def _g_phi(x):
        """Replacement function for B_phi calculation from virial_B"""
        return np.exp(-x)

    def B_phi(self, m):
        """Second virial coefficient for activity"""
        return self.virial_B(m, func=self._g_phi)

    def B_gamma(self, m):
        """Second virial coefficient for activity"""
        return self.B_phi(m) + self.virial_B(m, func=self.g)

    def f_phi(self, m):
        """Debye factor for osmotic coefficient"""
        sqrtI = ionic_strength(self.solute, m=m)**(1 / 2)
        return -self.A_phi * sqrtI / (1 + b * sqrtI)

    def f_gamma(self, m):
        """Debye factor for activity coefficient"""
        sqrtI = ionic_strength(self.solute, m=m)**(1 / 2)
        a1 = sqrtI / (1 + b * sqrtI)
        a2 = (2 / b) * np.log(1 + b * sqrtI)
        return -self.A_phi * (a1 + a2)

    def osmotic_coefficient(self, m):
        """Osmotic coefficient, phi"""
        coeff = self._activity_coeff(
            m,
            f=self.f_phi(m),
            B=self.B_phi(m),
            C=self.C_phi,
        )
        return 1 + coeff

    def water_activity(self, m):
        """Water activity, aw"""
        phi = self.osmotic_coefficient(m)
        return np.exp(-phi * Mw * self.nu_mx * m)

    def activity_coefficient(self, m):
        """Activity coefficient, gamma"""
        ln_gamma = self._activity_coeff(
            m,
            f=self.f_gamma(m),
            B=self.B_gamma(m),
            C=self.C_gamma,
        )
        return np.exp(ln_gamma)

    def solute_activity(self, m):
        """Solute activity, as = m * gamma"""
        gamma = self.osmotic_coefficient(m)
        return gamma * m
