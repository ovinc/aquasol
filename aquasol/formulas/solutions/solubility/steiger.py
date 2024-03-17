"""Steiger formulas for solubility of solutions.

Sources
-------
- Steiger, M.,
  Crystal growth in porous materials—I:
  The crystallization pressure of large crystals.
  Journal of Crystal Growth 282, 455-469 (2005).
  Valid at 25°C and up to 13.5 mol/kg

- Steiger, M., Kiekbusch, J. & Nicolai,
  An improved model incorporating Pitzer's equations for calculation of
  thermodynamic properties of pore solutions implemented into an efficient
  program code.
  Construction and Building Materials 22, 1841-1850 (2008).

(some info of domain of validity of expressions in the following paper:)
Dorn, J. & Steiger, M. Measurement and Calculation of Solubilities in the
Ternary System NaCH 3 COO + NaCl + H 2 O from 278 K to 323 K.
J. Chem. Eng. Data 52, 1784-1790 (2007).)
"""

import numpy as np
from pynverse import inversefunc

from ....constants import dissociation_numbers
from ....format import make_array_method
from ...general import SaturatedSolutionFormula
from ..steiger import coeffs_steiger2008_activity
from ..steiger import coeffs_steiger2008_solubility
from ..pitzer import PitzerActivity


# NOTE: KCl and Na2SO4 do not behave nicely for now --> INVESTIGATE


class Solubility_Steiger_Base(SaturatedSolutionFormula):

    source = 'Steiger 2008'

    concentration_unit = 'm'

    temperature_unit = 'K'
    temperature_range = (0 + 273.15, 50 + 273.15)

    def _solubility_product(self, T):
        ln_K = coeffs_steiger2008_solubility.ln_K(crystal=self.crystal, T=T)
        return np.exp(ln_K)

    def _solute_activity(self, m, T):
        """Incorporates water activity if hydrated crystal"""
        coeffs = coeffs_steiger2008_activity.coeffs(solute=self.solute, T=T)
        pitz = PitzerActivity(T=T, solute=self.solute, **coeffs)
        gamma = pitz.activity_coefficient(m=m)

        nu_m, nu_x = dissociation_numbers[self.solute]
        nu = nu_m + nu_x

        if self.crystal_hydration:
            nu_w = self.crystal_hydration
            a_w = pitz.water_activity(m=m)
            K_w = a_w ** nu_w
        else:
            K_w = 1

        return nu_m**nu_m * nu_x**nu_x * (gamma * m)**nu * K_w


    @make_array_method
    def calculate(self, T):
        """Make array because the inversion needs to be made at each temperature."""

        def _solute_activity(m):
            return self._solute_activity(m, T)

        _solute_molality = inversefunc(_solute_activity, domain=[0, 8])

        K = self._solubility_product(T)
        m = _solute_molality(K)

        return m


# =============================== Steiger 2008 ===============================


class Solubility_NaCl_Steiger2008_Base(Solubility_Steiger_Base):
    crystal = 'NaCl'


class Solubility_NaCl_2H2O_Steiger2008_Base(Solubility_Steiger_Base):
    crystal = 'NaCl,2H2O'
    crystal_hydration = 2

    # Unsure of Tmin, but definitely its stability stops at 0.1°C
    temperature_range = (-20 + 273.15, 0.1 + 273.15)


class Solubility_Na2SO4_Steiger2008_Base(Solubility_Steiger_Base):
    """Thenardite"""
    crystal = 'Na2SO4'


class Solubility_Na2SO4_10H2O_Steiger2008_Base(Solubility_Steiger_Base):
    """Mirabilite"""
    crystal = 'Na2SO4,10H2O'
    crystal_hydration = 10

    # Mirabilite stable zone stops at 32.38°C
    temperature_range = (0 + 273.15, 32.38 + 273.15)


class Solubility_KCl_Steiger2008_Base(Solubility_Steiger_Base):
    crystal = 'KCl'
