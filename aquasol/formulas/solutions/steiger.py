"""Various tools to calculate solution activities using Steiger formulae."""

import json
from copy import deepcopy
from pathlib import Path

import numpy as np

from ...constants import dissociation_numbers


# corrective factors between 2005 / 2008 for 1:1 and 2:1 electrolytes
c_11 = 2
c_21 = 4 / 2**(1 / 2)

# Correspondence between number of ions and corrective factor
pitzer_corr = {2: c_11, 3: c_21}


class CoeffsSteiger2005_Activity:
    """Load and manage Steiger 2005 coefficients for activity"""

    file = 'Coeffs_Steiger2005_Activity.json'

    def __init__(self):
        """Load and format raw coefficients stored in json file."""
        path = Path(__file__).parent / 'data' / self.file
        with open(path, 'r', encoding='utf8') as file:
            self.all_coeffs = json.load(file)

    def coeffs(self, solute='NaCl', T=298.15):
        """Get beta, C, A_phi, etc. coefficients at 298.15K for a given solute"""
        coeffs = self.all_coeffs[solute]
        coeffs['A_phi'] = self.all_coeffs['A_phi']
        return coeffs


class CoeffsSteiger2008:
    """Load and manage Steiger 2008 coefficients for activity and solubility

    (base class)
    """

    file = None  # define in subclasses

    def __init__(self):
        """Load and format raw coefficients stored in json file."""
        path = Path(__file__).parent / 'data' / self.file
        with open(path, 'r', encoding='utf8') as file:
            raw_coeffs = json.load(file)
        self.all_coeffs = self._format_coeffs(raw_coeffs)

    @staticmethod
    def _calculate_parameter(T, *coeffs):
        """Determine betas or third virial coefficient C as a function of T.

        Note: is also used to calculate solubility as a function of T.
        (see solutions.saturated)
        """
        Tr = 298.15
        q1, q2, q3, q4, q5, q6 = coeffs
        term2 = q2 * (1 / T - 1 / Tr)
        term3 = q3 * np.log(T / Tr)
        term4 = q4 * (T - Tr)
        term5 = q5 * (T ** 2 - Tr ** 2)
        term6 = q6 * np.log(T - 225)
        return q1 + term2 + term3 + term4 + term5 + term6


class CoeffsSteiger2008_Activity(CoeffsSteiger2008):
    """Load and manage Steiger 2008 coefficients for activity"""

    file = 'Coeffs_Steiger2008_Activity.json'

    @staticmethod
    def _format_coeffs(raw_coeffs):
        """Take into account corrective factors depending on dissociation numbers."""
        all_coeffs = deepcopy(raw_coeffs)
        A_phi = all_coeffs.pop('A_phi')
        for solute, coeffs in all_coeffs.items():
            c_phi = coeffs.pop('C_phi')
            nu_mx = sum(dissociation_numbers[solute])
            corr = pitzer_corr[nu_mx]
            coeffs['C_phi'] = [corr * q for q in c_phi]
        all_coeffs['A_phi'] = A_phi
        return all_coeffs

    def A_phi(self, T=298.15):
        """Debye-Huckel parameter as a function of the temperature T at 0.1MPa"""
        a1, a2, a3, a4, a5, a6 = self.all_coeffs['A_phi']
        return a1 + a2 / (T - 222) + a3 / T**2 + a4 * T + a5 * T**2 + a6 * T**4

    def coeffs(self, solute='NaCl', T=298.15):
        """Get beta, C, A_phi, etc. coefficients ata a given temperature for a given solute"""
        coeffs = {}
        coeffs['A_phi'] = self.A_phi(T)
        for name in 'beta0', 'beta1', 'beta2', 'C_phi':
            qs = self.all_coeffs[solute][name]
            coeffs[name] = self._calculate_parameter(T, *qs)
        for name in 'alpha1', 'alpha2':
            coeffs[name] = self.all_coeffs[solute][name]
        return coeffs


class CoeffsSteiger2008_Solubility(CoeffsSteiger2008):
    """Load and manage Steiger 2008 coefficients for solubility"""

    file = 'Coeffs_Steiger2008_Solubility.json'

    @staticmethod
    def _format_coeffs(raw_coeffs):
        """Take into account corrective factors depending on dissociation numbers."""
        return raw_coeffs

    def ln_K(self, crystal='NaCl', T=298.15):
        return self._calculate_parameter(T, *self.all_coeffs[crystal])


coeffs_steiger2005_activity = CoeffsSteiger2005_Activity()
coeffs_steiger2008_activity = CoeffsSteiger2008_Activity()
coeffs_steiger2008_solubility = CoeffsSteiger2008_Solubility()
