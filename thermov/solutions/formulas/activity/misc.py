"""Various functions for calculation of the water activity of solutions."""


from numpy import exp, log

from ....constants import Tc


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

