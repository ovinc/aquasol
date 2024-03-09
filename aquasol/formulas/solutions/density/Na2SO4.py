"""Gathers the formulas for the density of Na2SO4 solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns two parameters:
- rho0, density of pure water in kg / m^3
- rho, density of solution in kg / m^3
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------

- Tang, I. N. & Munkelwitz, H. R.
  Simultaneous Determination of Refractive Index and Density of an
  Evaporating Aqueous Solution Droplet.
  Aerosol Science and Technology 15, 201-207 (1991).

- Krumgalz, B. S., Pogorelsky, R. & Pitzer, K. S.
  Volumetric Properties of Single Aqueous Electrolytes from Zero to Saturation
  Concentration at 298.15 °K Represented by Pitzer's Ion-Interaction Equations.
  Journal of Physical and Chemical Reference Data 25, 663-689 (1996).

- Clegg, S. L. & Wexler, A. S.
  Densities and Apparent Molar Volumes of Atmospherically Important
  Electrolyte Solutions. 1. The Solutes H2SO4, HNO3, HCl, Na2SO4, NaNO3, NaCl,
  (NH4)2SO4, NH4NO3, and NH4Cl from 0 to 50 °C, Including Extrapolations to
  Very Low Temperature and to the Pure Liquid State, and NaHSO4, NaOH, and NH3
  at 25 °C. J. Phys. Chem. A 115, 3393-3460 (2011).
"""

import numpy as np

from ...general import SolutionFormula
from ...water.density_atm import DensityAtm_IAPWS

from .clegg import density_Na2SO4_high_conc
from .krumgalz import Density_Na2SO4_Krumgalz_Base
from .misc import rho_tang


class Density_Na2SO4_Tang(SolutionFormula):

    source ='Tang'
    solute = 'Na2SO4'

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'w'
    concentration_range = (0, 0.68)

    default = True
    with_water_reference = True

    coeffs = np.array([8.871e-3, 3.195e-5, 2.28e-7, 0]) * 1000

    def calculate(self, w, T):
        return rho_tang(w, self.coeffs)


class Density_Na2SO4_Krumgalz(Density_Na2SO4_Krumgalz_Base):
    """Already defined in Krumgalz module and not default here"""
    pass


class Density_Na2SO4_Clegg(SolutionFormula):

    source ='Clegg'
    solute = 'Na2SO4'

    temperature_unit = 'K'
    temperature_range = (273.15, 348.15)  # 0°C to 75°C

    concentration_unit = 'w'
    concentration_range = (0.22, 1)

    with_water_reference = True

    def calculate(self, w, T):
        density_atm = DensityAtm_IAPWS()
        rho_w = density_atm.calculate(T=T)
        # NOTE : there is also a formula that I coded for low concentration
        # but there seems to be a problem somewhere because it's not continuous
        # with the high concentration formula
        # (see clegg.py module)
        return rho_w, density_Na2SO4_high_conc(w, T)



# ========================== WRAP-UP OF FORMULAS =============================

Density_Na2SO4_Formulas = (
    Density_Na2SO4_Tang,
    Density_Na2SO4_Krumgalz,
    Density_Na2SO4_Clegg,
)