"""Functions to calculate the surface tension of water as a function of T.

Sources
-------
IAPWS, Release on Surface Tension of Ordinary Water Substance,
IAPWS, London, September 1994.
"""

from ...constants import Tc


# General Info about the formulas

default_source = 'IAPWS'

temperature_units = {'IAPWS': 'K'}

temperature_ranges = {'IAPWS': (248.15, Tc)}   # Here I have included the extrapolated range

def sigma_iapws(T):
    """Formula of surface tension according to IAPWS.

    Input
    -----
    Temperature in K

    Output
    ------
    Surface tension in N/m

    Reference
    ---------
    IAPWS, Release on Surface Tension of Ordinary Water Substance,
    IAPWS, London, September 1994.

    Notes
    -----
    - Used by Conde2004 and Dutcher2010 for the surface tension of solutions.
    - Valid between triple point (0.01°C) and critical temperature 647.096K.
    It also provides reasonably accurate values when extrapolated into the
    supercooled region, to temperatures as low as -25°C.
    """
    tau = (1 - T / Tc)

    B = 235.8e-3
    b = -0.625
    mu = 1.256

    sigma = B * tau ** mu * (1 + b * tau)  # in N / m

    return sigma


# ========================== WRAP-UP OF FORMULAS =============================

formulas = {'IAPWS': sigma_iapws}

sources = [source for source in formulas]
