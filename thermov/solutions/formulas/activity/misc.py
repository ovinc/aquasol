"""Various functions for calculation of the water activity of solutions."""


from numpy import exp

from ....constants import Tc, charge_numbers
from ...convert import ion_quantities, ionic_strength


def aw_conde(w, T, coeffs):
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
    International Journal of Thermal Sciences 43, 367–382 (2004).
    """

    pi0, pi1, pi2, pi3, pi4, pi5, pi6, pi7, pi8, pi9 = coeffs

    a = 2 - (1 + (w / pi0)**pi1)**pi2
    b = (1 + (w / pi3)**pi4)**pi5 - 1

    t = T / Tc

    f = a + b * t
    pi25 = 1 - (1 + (w / pi6)**pi7)**pi8 - pi9 * exp(-(w - 0.1)**2 / 0.005)

    return f * pi25

def aw_clegg(x, T, solute, coeffs):

    x_ion1, x_ion2 = ion_quantities(solute, x=x)
    x1 = 1 - (x_ion1 + x_ion2)  # mole fraction of water

    z_ion1, z_ion2 = charge_numbers[solute]

    Ix = ionic_strength(solute, x=x)  # ionic strength

    rho = 13.0
    
    A_x, B, alpha, W1, U1, V1 = coeffs

    val = 2 * A_x * Ix**(3 / 2) / (1 + rho * Ix**(1 / 2))  # 1st line
    val -= x_ion1 * x_ion2 * B * exp(-alpha * Ix**(1 / 2))  # 2nd line
    val += (1 - x1) * x_ion2 * (1 + z_ion2) * W1  # 5th line
    val += (1 - 2 * x1) * x_ion1 * x_ion2 * ((1 + z_ion2)**2 / z_ion2) * U1  # 6-7th lines
    val += 4 * x1 * (2 - 3 * x1) * x_ion1 * x_ion2 * V1  # 8th line

    f1 = exp(val)
    a1 = f1 * x1

    return a1