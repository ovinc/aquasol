"""Properties of pure water."""

from ..properties import WaterProperty

from ..formulas.water.density_atm import DensityAtmFormulas
from ..formulas.water.density_sat import DensitySatFormulas
from ..formulas.water.diffusivity_in_air import DiffusivityInAirFormulas
from ..formulas.water.surface_tension import SurfaceTensionFormulas
from ..formulas.water.vapor_pressure import VaporPressureFormulas
from ..formulas.water.viscosity_atm import ViscosityAtmFormulas


class DensityAtm(WaterProperty):
    """Density of ambient pure water as a function of temperature [kg/m^3].

    Examples
    --------
    >>> from aquasol.water import density_sat as rho
    >>> rho()  # returns the density of water (rho) at 25°C
    >>> rho(20)                  # rho  at 20°C
    >>> rho([0, 10, 20, 30])     # rho at various temperatures in Celsius
    >>> rho(300, 'K')            # rho at 300K
    """

    quantity = 'density (sat.)'
    unit = '[kg/m^3]'

    Formulas = DensityAtmFormulas


class DensitySat(WaterProperty):
    """Density of saturated liquid water as a function of temperature [kg/m^3].

    Examples
    --------
    >>> from aquasol.water import density_sat as rho
    >>> rho()  # returns the denisty of water (rho) at 25°C
    >>> rho(20)                  # rho  at 20°C
    >>> rho([0, 10, 20, 30])     # rho at various temperatures in Celsius
    >>> rho(300, 'K')            # rho at 300K
    """

    quantity = 'density (sat.)'
    unit = '[kg/m^3]'

    Formulas = DensitySatFormulas


class DiffusivityInAir(WaterProperty):
    """Diffusivity of water vapor as a function of temperature [m^2/s].

    Examples
    --------
    >>> from aquasol.water import diffusivity_in_air as d
    >>> d()  # returns the diffusivity of water in air at 25°C
    >>> d(20)                  # at 20°C
    >>> d([0, 10, 20, 30])     # at various temperatures in Celsius
    >>> d(300, 'K')            # at 300K
    """

    quantity = 'vapor diffusivity in air'
    unit = '[m^2/s]'

    Formulas = DiffusivityInAirFormulas


class SurfaceTension(WaterProperty):
    """Surface tension of pure water as a function of temperature [N/m]

    Examples
    --------
    >>> from aquasol.water import surface_tension as sigma
    >>> sigma()  # returns the surface tension of water (sigma) at 25°C
    >>> sigma(20)                  # sigma  at 20°C
    >>> sigma([0, 10, 20, 30])     # sigma at various temperatures in Celsius
    >>> sigma(300, 'K')            # sigma at 300K
    """

    quantity = 'surface tension'
    unit = '[N/m]'

    Formulas = SurfaceTensionFormulas


class VaporPressure(WaterProperty):
    """Saturation vapor pressure of water as a function of temperature [Pa]

    Examples
    --------
    >>> from aquasol.water import vapor_pressure as psat
    >>> psat()  # returns the saturation vapor pressure of water at 25°C
    >>> psat(20)                   # at 20°C
    >>> psat([0, 10, 20, 30])      # at various temperatures in Celsius
    >>> psat(300, 'K')             # at 300K
    >>> psat(15, source='Wexler')  # at 15°C using Wexler equation
    """

    quantity = 'saturated vapor pressure'
    unit = '[Pa]'

    Formulas = VaporPressureFormulas


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

    Formulas = ViscosityAtmFormulas


density_atm = DensityAtm()
density_sat = DensitySat()
diffusivity_in_air = DiffusivityInAir()
surface_tension = SurfaceTension()
vapor_pressure = VaporPressure()
viscosity_atm = ViscosityAtm()
