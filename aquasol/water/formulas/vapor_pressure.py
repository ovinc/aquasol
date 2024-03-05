"""Functions to calculate the vapor pressure of water as a function of
temperature using NIST or IAPWS recommended equations.

Notes
-----
Some older references use different scales of temperatures (e.g. IPS68 / 90)
which might be why some values for the critical point are slightly different.
Here we consider all absolute temperatures as being in Kelvin.
"""

from dataclasses import dataclass

import numpy as np

from ...constants import Tc, Patm, Pc, Tc




class VaporPressure_Wexler(WaterFormula):
    """Water Saturation pressure according to Wexler 1971, eq. (17). T in K."""

    name = 'Wexler'
    source_name = 'Wexler'

    temperature_unit = 'K'
    temperature_range = (273.15, 373.15)

    coeffs = {
        'E':
            [
                -7.51152e3,
                9.65389644e1,
                2.399897e-2,
                -1.1654551e-5,
                -1.2810336e-8,
                2.0998405e-11,
            ],
        'B': -1.2150799e1
    }

    def calculate(self, T):
        lnp = self.coeffs['B'] * np.log(T)
        for i, e in enumerate(self.coeffs['E']):
            lnp += e * T**(i - 1)
        return np.exp(lnp)


class VaporPressure_Bridgeman(WaterFormula):
    """Water Saturation pressure according to Bridgeman 1964. T in C."""

    name = 'Bridgeman'
    source_name = 'Bridgeman'

    temperature_unit = 'C'
    temperature_range = (0, 374.15)

    coeffs = {
        'A': 1.06423320,
        'B': 1.0137921,
        'C': 5.83531e-4,
        'D': 4.16385282,
        'E': 237.098157,
        'F': 0.30231574,
        'G': 3.377565e-3,
        'H': 1.152894,
        'K': 0.745794,
        'L': 654.2906,
        'M': 266.778,
        'Tx': 187,
    }

    def calculate(self, T):
        A, B, C, D, E, F, G, H, K, L, M, Tx = self.coeffs.values()

        Y1 = D * (T - Tx) / (T + E)
        X = (T - Tx) / 100
        Z = Tx / 100 * (-1 + 2 * (H - K * np.arccosh(L / (T + M))))
        a = Z**2 * ((Tx / 100)**2 - Z**2) / (F * (1 + G * T))

        yfact = 3 * np.sqrt(3) / (2 * (Tx / 100)**3)
        Y2 =  yfact * (X - 0.01 * a) * ((Tx / 100)**2 - (X - 0.01 * a)**2) / 100

        logp = A + Y1 - B * (1 + C * T) * Y2

        return (10**logp) * Patm


class VaporPressure_Wagner(WaterFormula):
    """Water saturation pressure according to Wagner & Pruß, T in K."""

    name = 'Wagner'
    source_name = 'Wagner'

    temperature_unit = 'K'
    temperature_range = (273.15, Tc)  # in fact 273.16 (triple point)

    coeffs = [
        -7.85951783,
        1.84408259,
        -11.7866497,
        22.6807411,
        -15.9618719,
        1.80122502
    ]

    def calculate(self, T):
        v = 1 - T / Tc
        a1, a2, a3, a4, a5, a6 = self.coeffs

        val = Tc / T * (a1 * v + a2 * v**1.5 + a3 * v**3 + a4 * v**3.5 + a5 * v**4 + a6 * v**7.5)

        return np.exp(val) * Pc




# ========================== WRAP-UP OF FORMULAS =============================


class VaporPressure(WaterProperty):

    formulas = (
        VaporPressure_Wexler,
        VaporPressure_Bridgeman,
        VaporPressure_Wagner
    )

    default_formula = VaporPressure_Wagner
