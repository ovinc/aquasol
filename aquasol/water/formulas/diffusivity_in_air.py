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

# General Info about the formulas

default_source = 'Massman'

temperature_units = {'Massman': 'K',
                     'MM72': 'K',
                     }

temperature_ranges = {'Massman': (273.15, 373.15),
                      'MM72': (273.15, 373.15),
                      }


def diffusivity_massman(T):
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
    T0 = 273.15   # K
    return (0.2178 * (T / T0) ** 1.81) * 1e-4


def diffusivity_mm72(T):
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
    T0 = 273.15   # K
    return (0.209 * (T / T0) ** 2.072) * 1e-4


# ========================== WRAP-UP OF FORMULAS =============================


formulas = {'Massman': diffusivity_massman,
            'MM72': diffusivity_mm72,
            }

sources = [source for source in formulas]
