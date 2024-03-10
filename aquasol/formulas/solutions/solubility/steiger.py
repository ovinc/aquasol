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
    temperature_range = (0 + 273.15, 45 + 273.15)

    def _solubility_product(self, T):
        ln_K = coeffs_steiger2008_solubility.ln_K(solute=self.solute, T=T)
        return np.exp(ln_K)

    def _solute_activity(self, m, T):

        # In case of hydrated phases:
        try:
            solute, _ = self.solute.split('-')
        except ValueError:  # not hydrated (solute=crystal)
            solute = self.solute

        coeffs = coeffs_steiger2008_activity.coeffs(solute=solute, T=T)
        pitz = PitzerActivity(T=T, solute=solute, **coeffs)
        gamma = pitz.activity_coefficient(m=m)
        return (gamma * m)**2

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
    solute = 'NaCl'


class Solubility_Na2SO4_Steiger2008_Base(Solubility_Steiger_Base):
    solute = 'Na2SO4'


class Solubility_Na2SO4_10H2O_Steiger2008_Base(Solubility_Steiger_Base):
    solute = 'Na2SO4'
    crystal_hydration = 2


class Solubility_KCl_Steiger2008_Base(Solubility_Steiger_Base):
    solute = 'KCl'
