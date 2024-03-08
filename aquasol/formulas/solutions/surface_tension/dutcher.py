"""Dutcher formula for the surface tension of NaCl solutions.

Source
------
- Dutcher: Dutcher, C. S., Wexler, A. S. & Clegg, S. L.
  Surface Tensions of Inorganic Multicomponent Aqueous Electrolyte Solutions and Melts.
  J. Phys. Chem. A 114, 12216-12230 (2010).
"""

import numpy as np

from ...general import SolutionFormula
from .misc import sigma_iapws


def sigma_dutcher(x, T, coeffs_table3, coeffs_table5):
    """General formula for surface tension accorging to Dutcher 2010.

    Valid for many solutes including NaCl, KCl, HCl, Na2S04, CaCl2, etc.

    Inputs
    ------
    x: mole fraction of salt
    T: temperature in K
    coeffs_table3: tuple or list of coefficients c1, c2 from table 3
    coeffs_table5: tuple or list of coefficients aws, bws, asw, bsw (table 5)

    Outputs
    -------
    Surface tension of solution, N/m

    Notes
    -----
    - Validity range for temperature and concentration are given in Table 2.
    - The original paper has a value for the critical point of water slightly
    off (647.15 instead of 647.096), but the difference is not noticeable.
    This value is used in the calculation of the surface tension of pure water
    from the IAPWS formula.

    Reference
    ---------
    Dutcher: Dutcher, C. S., Wexler, A. S. & Clegg, S. L. Surface Tensions of
    Inorganic Multicomponent Aqueous Electrolyte Solutions and Melts.
    J. Phys. Chem. A 114, 12216-12230 (2010).
    """

    # Coefficients of Table 3
    c1, c2 = coeffs_table3
    # Coefficients of Table 5
    aws, bws, asw, bsw = coeffs_table5

    xw = 1 - x  # mole fraction of water

    # Surface tension of water (Eq. 10)
    gw = sigma_iapws(T) * 1e3    # in mN / m

    # Surface tension of molten salt (Eq. 12)
    gs = c1 + c2 * T    # in mN / m

    # Surface tension of solution (Eq. 5)
    Fws = aws + bws * T
    Fsw = asw + bsw * T
    gna = np.exp(xw * np.log(gw + Fws * x) + x * np.log(gs + Fsw * xw))  # mN / m

    return gna * 1e-3


def coeffs_CaCl2():

    # Coefficients (Table 3)
    c1 = 195.67     # note - other values possible: (189, -0.03952)
    c2 = -0.04541
    # Coefficients (Table 5)
    aws = -19.766
    bws = 0.575
    asw = 0
    bsw = 0

    coeffs_table3 = c1, c2
    coeffs_table5 = aws, bws, asw, bsw

    return coeffs_table3, coeffs_table5


def coeffs_KCl():

    # Coefficients (Table 3)
    c1 = 177.61
    c2 = -0.07519
    # Coefficients (Table 5)
    aws = -117.33
    bws = 0.489
    asw = 0
    bsw = 0

    coeffs_table3 = c1, c2
    coeffs_table5 = aws, bws, asw, bsw

    return coeffs_table3, coeffs_table5


def coeffs_MgCl2():

    # Coefficients (Table 3)
    c1 = 65.343
    c2 = -0.003073
    # Coefficients (Table 5)
    aws = 1069.9
    bws = -2.86
    asw = 0
    bsw = 0

    coeffs_table3 = c1, c2
    coeffs_table5 = aws, bws, asw, bsw

    return coeffs_table3, coeffs_table5


def coeffs_Na2SO4():

    # Coefficients (Table 3)
    c1 = 269
    c2 = -0.066
    # Coefficients (Table 5)
    aws = 126
    bws = 0
    asw = -194.45
    bsw = 0

    coeffs_table3 = c1, c2
    coeffs_table5 = aws, bws, asw, bsw

    return coeffs_table3, coeffs_table5


def coeffs_NaCl():

    # Coefficients (Table 3)
    c1 = 191.16     # note - other values possible: (193.48, -0.07188)
    c2 = -0.0747
    # Coefficients (Table 5)
    aws = 232.54
    bws = -0.245
    asw = -142.42
    bsw = 0

    coeffs_table3 = c1, c2
    coeffs_table5 = aws, bws, asw, bsw

    return coeffs_table3, coeffs_table5


class SurfaceTension_Dutcher_Base(SolutionFormula):

    source ='Dutcher'

    temperature_unit = 'K'
    concentration_unit = 'x'

    with_water_reference = True

    def calculate(self, x, T):
        """Surface tension calculated from Dutcher 2010.
        Input: mole fraction x, temperature T in K."""
        sigma_w = sigma_iapws(T)
        sigma = sigma_dutcher(x, T, *self.coeffs)

        return sigma_w, sigma


class SufaceTension_CaCl2_Dutcher_Base(SurfaceTension_Dutcher_Base):
    solute = 'CaCl2'
    temperature_range = (243.15, 373.15)
    concentration_range = (0, 0.117)
    coeffs = coeffs_CaCl2()


class SufaceTension_KCl_Dutcher_Base(SurfaceTension_Dutcher_Base):
    solute = 'KCl'
    temperature_range = (265.15, 353.15)
    concentration_range = (0, 0.138)  # Estimated from m_max = 8.86
    coeffs = coeffs_KCl()


class SufaceTension_MgCl2_Dutcher_Base(SurfaceTension_Dutcher_Base):
    solute = 'MgCl2'
    temperature_range = (283.15, 343.15)
    concentration_range = (0, 0.0944)
    coeffs = coeffs_MgCl2()


class SufaceTension_Na2SO4_Dutcher_Base(SurfaceTension_Dutcher_Base):
    solute = 'Na2SO4'
    temperature_range = (273.15, 466.55)
    concentration_range = (0, 0.0446)
    coeffs = coeffs_Na2SO4()


class SufaceTension_NaCl_Dutcher_Base(SurfaceTension_Dutcher_Base):
    solute = 'NaCl'
    temperature_range = (263.13, 473.15)
    concentration_range = (0, 0.145)
    coeffs = coeffs_NaCl()
