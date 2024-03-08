"""Krumgalz density formulas for different salts

Source
------
- Krumgalz, B. S., Pogorelsky, R. & Pitzer, K. S.
  Volumetric Properties of Single Aqueous Electrolytes from Zero to Saturation
  Concentration at 298.15 °K Represented by Pitzer's Ion-Interaction Equations.
  Journal of Physical and Chemical Reference Data 25, 663-689 (1996).
"""

import numpy as np

from ...general import SolutionFormula
from .misc import density_pitzer

class Density_Krumgalz_Base(SolutionFormula):

    source ='Krumgalz'

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'm'

    with_water_reference = True

    def calculate(self, m, T):
        return density_pitzer(m, solute=self.solute, source='Krumgalz')


class Density_CaCl2_Krumgalz_Base(Density_Krumgalz_Base):
    solute = 'CaCl2'
    concentration_range = (0, 7.7)


class Density_KCl_Krumgalz_Base(Density_Krumgalz_Base):
    solute = 'KCl'
    concentration_range = (0, 4.7)


class Density_KI_Krumgalz_Base(Density_Krumgalz_Base):
    solute = 'KI'
    concentration_range = (0, 8.6)


class Density_LiCl_Krumgalz_Base(Density_Krumgalz_Base):
    solute = 'LiCl'
    concentration_range = (0, 19.6)


class Density_MgCl2_Krumgalz_Base(Density_Krumgalz_Base):
    solute = 'MgCl2'
    concentration_range = (0, 5.8)


class Density_Na2SO4_Krumgalz_Base(Density_Krumgalz_Base):
    solute = 'Na2SO4'
    concentration_range = (0, 1.5)


class Density_NaCl_Krumgalz_Base(Density_Krumgalz_Base):
    solute = 'NaCl'
    concentration_range = (0, 14)


