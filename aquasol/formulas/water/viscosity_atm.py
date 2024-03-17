"""Function to calculate the viscosity of liquid water as a function of T.

Sources
-------

--- 'IAPWS':
    Huber, M. L. et al.
    "New International Formulation for the Viscosity of H2O."
    Journal of Physical and Chemical Reference Data 38, 101-125
    (2009)
"""

from ..general import WaterFormula


class ViscosityAtm_IAPWS(WaterFormula):

    source ='IAPWS'
    temperature_unit = 'K'
    temperature_range = (253.15, 383.15)
    default = True

    def calculate(self, T):
        """Viscosity of liquid water according to Huber 2009 (IAPWS)

        Input
        -----
        Temperature in K

        Output
        ------
        Viscosity in Pa.s

        Reference
        ---------
        Huber, M. L. et al.
        New International Formulation for the Viscosity of H2O.
        Journal of Physical and Chemical Reference Data 38, 101-125 (2009).

        Notes
        -----
        - Valid between 253.15 K and 383.15 K (metastable domains included)
        """
        t = T / 300

        mu_1 = 280.68 * t ** (-1.9)
        mu_2 = 511.45 * t ** (-7.7)
        mu_3 = 61.131 * t ** (-19.6)
        mu_4 = .45903 * t ** (-40)

        return (mu_1 + mu_2 + mu_3 + mu_4) * 1e-6


# ========================== WRAP-UP OF FORMULAS =============================

ViscosityAtmFormulas = (
    ViscosityAtm_IAPWS,
)
