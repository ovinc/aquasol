"""Gathers the formulas for the electrical conductivity of KCl solutions.

Note
----
When adding source, make sure to make a function that has two parameters:
- w (weight fraction), range 0-1 or other concentration quantity
- T (temperature), in K
and returns one parameter
- sigma, electrical conductivity, in S/m
Also, add the name of the function to the formulas dictionary at the end of the
file.

Sources
-------
- McKee, C. B.
  An Accurate Equation for the Electrolytic Conductivity
  of Potassium Chloride Solutions.
  J Solution Chem 38, 1155-1172 (2009).
"""

import numpy as np

from ...general import SolutionFormula


# ============================== FORMULAS ====================================

# ----------------------------------- MC25 -----------------------------------


def mc25_flas(m):
    """Conductivity component FLAS from McKee 2009"""
    a = 111.732
    b = -6.01942e-2
    c = -2.03830e-3
    return a * np.exp(b * m + c * m**2)


def mc25_fmid(m):
    """Conductivity component FMID from McKee 2009"""
    a = 34.5286
    b = -2.25008
    return a * np.exp(b * m**(1/2))


def mc25_fini(m):
    """Conductivity component FINI from McKee 2009"""
    a = 1.45667
    b = -19.5946
    return a * np.exp(b * m)


def mc25_finii(m):
    """Conductivity component FINII from McKee 2009"""
    a = 0.960521
    b = -96.4192
    return a * np.exp(b * m)


def mc25_finiii(m):
    """Conductivity component FINIII from McKee 2009"""
    a = 0.587725
    b = -570.452
    return a * np.exp(b * m)


def mc25(m):
    """Conductivity, Total"""
    return mc25_flas(m) + mc25_fmid(m) + mc25_fini(m) + mc25_finii(m) + mc25_finiii(m)


# ------------------------------- MC50 / MC25 --------------------------------


fcon0 = 0.321662


def sol50re_flas(m):
    """Terms for MC50 / MC25, FLAS"""
    a = 0.165123
    b = -0.265938
    return a * np.exp(b * m)


def sol50re_fmid(m):
    """Terms for MC50 / MC25, FMID"""
    a = 1.57042e-2
    b = -2.16681
    return a * np.exp(b * m)


def sol50re_fini(m):
    """Terms for MC50 / MC25, FINI"""
    a = 8.26838e-3
    b = -26.7895
    return a * np.exp(b * m)


def sol50re_finii(m):
    """Terms for MC50 / MC25, FINII"""
    a = 2.99403e-3
    b = -525.162
    return a * np.exp(b * m)


def sol50re(m):
    """SOL50RE term"""
    return sol50re_flas(m) + sol50re_fmid(m) + sol50re_fini(m) + sol50re_finii(m)


def mc50_mc25(m):
    return 1 + fcon0 + sol50re(m)


# ------------------------ Temperature extrapolation -------------------------


def alpha_v(T):
    """ALPHA_V factor, T is temperature in deg. C"""
    b = -6.35249e-4
    c = 4.60006e-4
    d = -4.97223e-3
    e = -6.85638e-4
    return b + c * np.exp(d * T + e * T**2)


def alpha(T):
    """ALPHA factor, T is temperature in deg. C"""
    T1 = T - 25
    T2 = T - 50
    a = 4e-2
    return T1 * (a + T2 * alpha_v(T))


def beta_a_v(T):
    """BETAa_V factor, T is temperature in deg. C"""
    b = 1.21005e-3
    c = 6.64169e-4
    d = -2.64072e-3
    e = -7.78958e-4
    return b - c * np.exp(d * T + e * T**2)


def beta_a(T):
    """BETAa factor, T is temperature in deg. C"""

    T1 = T - 25
    T2 = T - 50
    a = 4e-2
    return T1 * (a + T2 * beta_a_v(T))


def beta_b_v(T):
    """BETAb_V factor, T is temperature in deg. C"""
    b = 4.44279e-4
    c = 3.35363e-4
    d = -3.04164e-3
    e = -6.99205e-4
    return b - c * np.exp(d * T + e * T**2)


def beta_b(T):
    """BETAb factor, T is temperature in deg. C"""
    T1 = T - 25
    T2 = T - 50
    return T1 * T2 * beta_b_v(T)


# ------------------------------- ALL TOGETHER -------------------------------

def mc_mc25(m, T):
    """MC / MC25"""
    return 1 + alpha(T) * fcon0 + (beta_a(T) + beta_b(T) * m) * sol50re(m)


def conductivity_KCl_McKee(m, T=25):
    return 0.1 * m * mc25(m) * mc_mc25(m, T)



class ElectricalConductivity_KCl_McKee(SolutionFormula):

    source ='McKee'
    solute = 'KCl'

    temperature_unit = 'C'
    temperature_range = (0, 55)

    concentration_unit = 'm'
    concentration_range = (0, 5)

    default = True
    with_water_reference = False

    def calculate(self, m, T):
        return conductivity_KCl_McKee(m=m, T=T)


# ========================== WRAP-UP OF FORMULAS =============================

ElectricalConductivity_KCl_Formulas = (
    ElectricalConductivity_KCl_McKee,
)
