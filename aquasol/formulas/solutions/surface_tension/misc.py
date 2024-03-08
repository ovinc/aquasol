"""MISC. formula for surface tension of solutions"""

import numpy as np

from ...water.surface_tension import SurfaceTension_IAPWS


def sigma_iapws(T):
    """T in K, IAPWS formula"""
    surface_tension_iapws = SurfaceTension_IAPWS()
    return surface_tension_iapws.calculate(T=T)
