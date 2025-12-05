"""Gathers the formulas for the viscosity of glycerol solutions.

Sources
-------
--- Takamura, K., Fischer, H. & Morrow, N. R.
    Physical properties of aqueous glycerol solutions.
    Journal of Petroleum Science and Engineering 98-99, 50-60 (2012).
"""

from ...general import SolutionFormula
from ...water.viscosity_atm import ViscosityAtm_IAPWS


water_viscosity = ViscosityAtm_IAPWS()


def k_zero(Tk):
    """Interaction coefficient (uses absolute temperature)"""
    return 4.74 - 0.012 * Tk


def viscosity_takamura(w, T):
    """Eq. (11) of Takamura et al.

    In the paper, Takamura et al. indicate that C is the volume fraction,
    but if one calculate the actual volume fraction it does not seem to work
    and if one puts weight fraction it works very well, so I have assumed
    that C = w.
    """
    Tk = T + 273.15
    mu0 = water_viscosity.calculate(T=Tk)
    k0 = k_zero(Tk)
    cm = 1.20
    x = w / cm
    y = k0 * cm
    a = (1 - x) / (1 - ((y - 1) * x))
    e = -2.5 * cm / (2 - y)
    mur = a ** e
    return mu0, mu0 * mur


class Viscosity_Glycerol_Takamura(SolutionFormula):
    """Viscosity of glycerol from Takamura"""

    default = True
    with_water_reference = True

    source = 'Takamura'
    solute = 'glycerol'

    temperature_unit = 'C'
    temperature_range = (20, 80)

    concentration_unit = 'w'
    concentration_range = (0, 1)

    def calculate(self, w, T):
        """Viscosity calculated from Takamura et al."""
        return viscosity_takamura(w=w, T=T)


# ========================== WRAP-UP OF FORMULAS =============================

ViscosityFormulas_Glycerol = (
    Viscosity_Glycerol_Takamura,
)
