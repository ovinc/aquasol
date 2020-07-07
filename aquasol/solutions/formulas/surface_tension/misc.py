"""Various functions for calculation of the surface tension of solutions."""


from numpy import exp, log

from ....constants import Tc

from ....water.formulas.surface_tension import sigma_iapws


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
    J. Phys. Chem. A 114, 12216–12230 (2010).
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
    gna = exp(xw * log(gw + Fws * x) + x * log(gs + Fsw * xw))  # mN / m

    return gna * 1e-3


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
    International Journal of Thermal Sciences 43, 367–382 (2004).

    """

    # surface tension of pure water
    sigma_w = sigma_iapws(T)

    # surface tension of the solution
    t = T / Tc
    s1, s2, s3, s4, s5 = coeffs
    r = 1 + s1 * w + s2 * w * t + s3 * w * t ** 2 + s4 * w ** 2 + s5 * w ** 3

    return sigma_w * r


