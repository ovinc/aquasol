"""Function that return the vapor pressure of water as a function of
temperature using NIST or IAPWS recommended equations"""

# TODO: Re-write examples for psat, not up to date !
# TODO: Write examples for surface tension


from .general import water_calculation


def psat(T, unit='C', source='Wagner'):
    """Return the vapor pressure (in Pascal) as a function of temperature.

    Parameters
    ----------
    - T (float): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - source (str, default None) : Source for the used equation, if None then
    gets the default source for the particular solute (defined in submodules).
    See summary of available sources below.

    Output
    ------
    - saturation vapor pressure (in Pa)

    Sources
    -------
    'Wagner' (default), 'Bridgeman', 'Wexler'
    (see submodules for details).

    Examples
    --------
    - psat(20) returns the vapor pressure of water at 20°C, using eq (17) of Wexler
    - psat(300, 'K') returns the value at 300K
    - psat(20, source='Wagner') returns the value at 20°C using Wagner equation
    - psat(300, 'K', 'Wagner') returns the value at 300K using Wagner equation
    """

    # Name of module containing the formulas for calculating vapor pressure.
    module = 'formulas.psat'

    # Calculate density using general solution calculation scheme ------------
    psat = water_calculation(source, module, T, unit)

    return psat


def surface_tension(T=25, unit='C', source='IAPWS'):
    """Surface tension (N/m) of pure water as a function of temperature.

    Parameters
    ----------
    - T (float): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - source (str, default None) : Source for the used equation, if None then
    gets the default source for the particular solute (defined in submodules).
    See summary of available sources below.

    Output
    ------
    Surface tension in N/m

    Sources
    -------
    'IAPWS' (default)
    (see submodules for details).
    """

    # Name of module containing the formulas for calculating vapor pressure.
    module = 'formulas.surface_tension'

    # Calculate surface tension using general solution calculation scheme ------------
    sigma = water_calculation(source, module, T, unit)

    return sigma




