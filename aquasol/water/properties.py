"""Properties of water (vapor pressure, surface tension, density) as a function of T."""


from .general import calculation
from ..format import format_output_type

def vapor_pressure(T=25, unit='C', source=None):
    """Return the vapor pressure (in Pascal) as a function of temperature.

    Parameters
    ----------
    - T (int, float, array, list, or tuple): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - source (str, default None) : Source for the used equation, if None then
    the default source for the particular property is used.

    Output
    ------
    - saturation vapor pressure (in Pa)

    Sources
    -------
    'Wagner' (default), 'Bridgeman', 'Wexler'
    (see submodules for details).

    Examples
    --------
    from thermov.water import vapor_pressure as psat
    >>> psat()  # returns the saturation vapor pressure of water at 25°C
    >>> psat(20)                   # at 20°C
    >>> psat([0, 10, 20, 30])      # at various temperatures in Celsius
    >>> psat(300, 'K')             # at 300K
    >>> psat(15, source='Wexler')  # at 15°C using Wexler equation

    """
    psat = calculation('vapor pressure', source, (T, unit))
    return format_output_type(psat)


def surface_tension(T=25, unit='C', source=None):
    """Surface tension (N/m) of pure water as a function of temperature.

    Parameters
    ----------
    - T (int, float, array, list, tuple): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - source (str, default None) : Source for the used equation, if None then
    the default source for the particular property is used.

    Output
    ------
    Surface tension in N/m

    Sources
    -------
    'IAPWS' (default)
    (see submodules for details).

    Examples
    --------
    >>> from thermov.water import surface_tension as sigma
    >>> sigma()  # returns the surface tension of water (sigma) at 25°C
    >>> sigma(20)                  # sigma  at 20°C
    >>> sigma([0, 10, 20, 30])     # sigma at various temperatures in Celsius
    >>> sigma(300, 'K')            # sigma at 300K
    """
    sigma = calculation('surface tension', source, (T, unit))
    return format_output_type(sigma)


def density_sat(T=25, unit='C', source=None):
    """Density (kg/m^3) of saturated liquid water as a function of temperature.

    Parameters
    ----------
    - T (int, float, array, list, tuple): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - source (str, default None) : Source for the used equation, if None then
    the default source for the particular property is used.

    Output
    ------
    Density in kg/m^3

    Sources
    -------
    'Wagner' (default)

    (see submodules for details).

    Examples
    --------
    >>> from thermov.water import density_sat as rho
    >>> rho()  # returns the denisty of water (rho) at 25°C
    >>> rho(20)                  # rho  at 20°C
    >>> rho([0, 10, 20, 30])     # rho at various temperatures in Celsius
    >>> rho(300, 'K')            # rho at 300K
    """
    rho = calculation('density saturated', source, (T, unit))
    return format_output_type(rho)


def density_atm(T=25, unit='C', source=None):
    """Density (kg/m^3) of ambient pure water as a function of temperature.

    Parameters
    ----------
    - T (int, float, array, list, tuple): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - source (str, default None) : Source for the used equation, if None then
    the default source for the particular property is used.

    Output
    ------
    Density in kg/m^3

    Sources
    -------
    'Patek' (default), Kell

    (see submodules for details).

    Examples
    --------
    >>> from thermov.water import density_sat as rho
    >>> rho()  # returns the denisty of water (rho) at 25°C
    >>> rho(20)                  # rho  at 20°C
    >>> rho([0, 10, 20, 30])     # rho at various temperatures in Celsius
    >>> rho(300, 'K')            # rho at 300K
    """
    rho = calculation('density ambient', source, (T, unit))
    return format_output_type(rho)
