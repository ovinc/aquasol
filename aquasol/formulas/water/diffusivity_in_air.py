"""Function to calculate the diffusivity in air as a function of temperature

Sources
-------

- Massman, W. J.
  A review of the molecular diffusivities of H2O, CO2, CH4, CO, O3, SO2, NH3,
  N2O, NO, and NO2 in air, O2 and N2 near STP.
  Atmospheric Environment 32, 1111-1127 (1998).

- Marrero, T. R. and Mason E. A.,
  Gaseous diffusion coeffcients.
  Journal of Physics and Chemistry Reference Data 1, 3-118 (1972)
"""

from ..general import WaterFormula


class DiffusivityInAir_Massman(WaterFormula):

    source ='Massman'
    temperature_unit = 'K'
    temperature_range = (273.15, 373.15)
    default = True

    coeffs = {'T0': 273.15}  # K

    def calculate(self,T):
        """Diffusivity of water vapor in air according to Massman 1998

        Input
        -----
        Temperature in K

        Output
        ------
        Diffusivity in m^2 / s

        Reference
        ---------
        Massman, W. J.
        A review of the molecular diffusivities of H2O, CO2, CH4, CO, O3, SO2, NH3,
        N2O, NO, and NO2 in air, O2 and N2 near STP.
        Atmospheric Environment 32, 1111-1127 (1998).

        Notes
        -----
        - Valid between 273.15 K and 373.15 K (0 to 100°C)
        """
        return (0.2178 * (T / self.coeffs['T0']) ** 1.81) * 1e-4


class DiffusivityInAir_MM72(WaterFormula):

    source ='MM72'
    temperature_unit = 'K'
    temperature_range = (273.15, 373.15)

    coeffs = {'T0': 273.15}  # K

    def calculate(self, T):
        """Diffusivity of water vapor in air according to Marrero & Mason (1972)

        (as reported in Massman 1998)

        Input
        -----
        Temperature in K

        Output
        ------
        Diffusivity in m^2 / s

        Reference
        ---------
        Marrero, T. R. and Mason E. A.,
        Gaseous diffusion coeffcients.
        Journal of Physics and Chemistry Reference Data 1, 3-118 (1972)

        Notes
        -----
        - Valid between 273.15 K and 373.15 K (0 to 100°C)
        """
        return (0.209 * (T / self.coeffs['T0']) ** 2.072) * 1e-4


# ========================== WRAP-UP OF FORMULAS =============================

DiffusivityInAirFormulas = (
    DiffusivityInAir_Massman,
    DiffusivityInAir_MM72
)
