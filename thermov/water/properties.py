"""Properties of water (vapor pressure, surface tension) as a function of T."""


from .general import calculation


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

    return calculation('vapor pressure', source, (T, unit))


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

    return calculation('surface tension', source, (T, unit))




