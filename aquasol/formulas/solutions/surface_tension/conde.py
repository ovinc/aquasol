"""Surface tension of solutions from Conde 2004

Source
------
Conde, M. R., Properties of aqueous solutions of lithium and calcium
chlorides: formulations for use in air conditioning equipment design.
International Journal of Thermal Sciences 43, 367-382 (2004).
"""

from ....constants import Tc
from ...general import SolutionFormula
from .misc import sigma_iapws


def sigma_conde(w, T, coeffs):
    """General formula for surface tension accorging to Conde IJTS 2004.

    Inputs
    ------
    w: weight fraction of salt
    T: temperature in K
    coeffs: coefficients sigma_i from Table 6
    coeffs_table5: tuple or list of coefficients aws, bws, asw, bsw (table 5)

    Outputs
    -------
    Surface tension of solution, N/m

    Notes
    -----
    Ranges of validity for temperature and concentration are given in Table 2.

    Reference
    ---------
    Conde, M. R., Properties of aqueous solutions of lithium and calcium
    chlorides: formulations for use in air conditioning equipment design.
    International Journal of Thermal Sciences 43, 367-382 (2004).
    """

    # surface tension of pure water
    sigma_w = sigma_iapws(T)

    # surface tension of the solution
    t = T / Tc
    s1, s2, s3, s4, s5 = coeffs
    r = 1 + s1 * w + s2 * w * t + s3 * w * t ** 2 + s4 * w ** 2 + s5 * w ** 3

    return sigma_w * r


class SurfaceTension_Conde_Base(SolutionFormula):

    source ='Conde'

    temperature_unit = 'K'
    temperature_range = (273.15, 373.15)

    concentration_unit = 'w'
    concentration_range = (0, 0.45)

    with_water_reference = True

    def calculate(self, w, T):
        """Surface tension calculated from Conde 2004.
        Input: weight fraction w, temperature T in K."""
        sigma_w = sigma_iapws(T)
        sigma = sigma_conde(w, T, self.coeffs)
        return sigma_w, sigma


class SurfaceTension_CaCl2_Conde_Base(SurfaceTension_Conde_Base):
    solute = 'CaCl2'
    coeffs = [2.33067, -10.78779, 13.56611, 1.95017, -1.77990]


class SurfaceTension_LiCl_Conde_Base(SurfaceTension_Conde_Base):
    solute = 'LiCl'
    coeffs = [2.757115, -12.011299, 14.751818, 2.443204, -3.147739]
