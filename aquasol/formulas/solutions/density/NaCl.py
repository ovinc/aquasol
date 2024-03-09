"""Gathers the formulas for the density of NaCl solutions.

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

- Simion (default) : "Mathematical modelling of density and
  viscosity of NaCl aqueous solutions" (2015). Valid from w = 0 to w = 0.26
  and for temperatures between 0 and 100°C

- Tang: "Chemical and size effects of hygroscopic aerosols on light
  scattering coefficients" (1996). Valid at 25°C and from w = 0 to w ~= 0.5

- Al Ghafri et al., Densities of Aqueous MgCl 2 (aq), CaCl 2 (aq), KI(aq),
  NaCl(aq), KCl(aq), AlCl 3 (aq), and (0.964 NaCl + 0.136 KCl)(aq) at
  Temperatures Between (283 and 472) K, Pressures up to 68.5 MPa, and
  Molalities up to 6 mol·kg -1.
  Journal of Chemical & Engineering Data 57, 1288-1304 (2012).

- Steiger:
  Talreja-Muthreja, T., Linnow, K., Enke, D. & Steiger, M.
  Deliquescence of NaCl Confined in Nanoporous Silica.
  Langmuir 38, 10963-10974 (2022).

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

from .clegg import density_NaCl
from .al_ghafri import Density_NaCl_AlGhafri_Base
from .krumgalz import Density_NaCl_Krumgalz_Base
from .misc import rho_tang, density_pitzer


class Density_NaCl_Simion(SolutionFormula):

    source ='Simion'
    solute = 'NaCl'

    temperature_unit = 'C'
    temperature_range = (0, 100)

    concentration_unit = 'w'
    concentration_range = (0, 0.27)

    default = True
    with_water_reference = True

    coeffs = {
        'a1': 750.2834,
        'a2': 26.7822,
        'a3': -0.26389,
        'a4': 1.90165,
        'a5': -0.11734,
        'a6': 0.00175,
        'a7': -0.003604,
        'a8': 0.0001701,
        'a9': -0.00000261,
    }

    def calculate(self, w, T):

        w = w * 100  # avoid using *= to not mutate objects in place
        T = T + 273.15  # same

        a1, a2, a3, a4, a5, a6, a7, a8, a9 = self.coeffs.values()

        rho0 = a1 + a4*T + a7*T**2  # density of pure water
        rho = rho0 + a2*w + a3*w**2 + (a5*w + a6*w**2) * T + (a8*w + a9*w**2) * T**2

        return rho0, rho

class Density_NaCl_Tang(SolutionFormula):

    source ='Tang'
    solute = 'NaCl'

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'w'
    concentration_range = (0, 0.5)

    with_water_reference = True

    coeffs = np.array([7.41e-3, -3.741e-5, 2.252e-6, -2.06e-8]) * 1000

    def calculate(self, w, T):
        return rho_tang(w, self.coeffs)


class Density_NaCl_AlGhafri(Density_NaCl_AlGhafri_Base):
    """Already defined in Al Ghafri module and not default here"""
    pass


class Density_NaCl_Steiger(SolutionFormula):

    source ='Steiger'
    solute = 'NaCl'

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'm'
    concentration_range = (0, 6.1)

    with_water_reference = True

    def calculate(self, m, T):
        return density_pitzer(m, solute='NaCl', source='Steiger')


class Density_NaCl_Krumgalz(Density_NaCl_Krumgalz_Base):
    """Already defined in Krumgalz module and not default here"""
    pass


class Density_NaCl_Clegg(SolutionFormula):

    source ='Clegg'
    solute = 'NaCl'

    temperature_unit = 'K'
    temperature_range = (273.15, 323.15)

    concentration_unit = 'w'
    concentration_range = (0.25, 1)

    with_water_reference = True

    def calculate(self, w, T):
        density_atm = DensityAtm_IAPWS()  # because used internally by Clegg
        rho_0 = density_atm.calculate(T)
        rho = density_NaCl(w, T)
        return rho_0, rho

# ========================== WRAP-UP OF FORMULAS =============================

Density_NaCl_Formulas = (
    Density_NaCl_Simion,
    Density_NaCl_Tang,
    Density_NaCl_AlGhafri,
    Density_NaCl_Steiger,
    Density_NaCl_Krumgalz,
    Density_NaCl_Clegg,
)