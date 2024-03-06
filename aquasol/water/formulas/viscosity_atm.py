"""Function to calculate the viscosity of liquid water as a function of T.

Sources
-------

- Huber, M. L. et al.
  New International Formulation for the Viscosity of H2O.
  Journal of Physical and Chemical Reference Data 38, 101-125 (2009).

"""

from ..general import WaterFormula, WaterProperty


class ViscosityAtm_Huber(WaterFormula):

    name = 'Huber'
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

class ViscosityAtm(WaterProperty):
    """Viscosity of water at ambient pressure as a function of temperature [Pa.s]

    Examples
    --------
    >>> from aquasol.water import viscosity_atm as mu
    >>> mu()  # returns the diffusivity of water in air at 25°C
    >>> mu(20)                  # at 20°C
    >>> mu([0, 10, 20, 30])     # at various temperatures in Celsius
    >>> mu(300, 'K')            # at 300K
    """

    quantity = 'viscosity (atm.)'
    unit = '[Pa.s]'

    Formulas = (
        ViscosityAtm_Huber,
    )
