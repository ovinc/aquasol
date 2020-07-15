"""Convert/invert some properties"""


# Non-standard imports
from pynverse import inversefunc

# Local imports
from ..format import format_inverse_result

from .properties import vapor_pressure


def dewpoint(T=25, unit='C', source=None, **humidity):
    """Inverts vapor_pressure() to calculate dew point at a given humidity.

    Inputs
    ------
    - T: value of temperature (default 25)
    - unit: temperature unit, can be 'C' or 'K' (default 'C')
    - source: literature source for the calculation (default: Auto)
    - humidity kwargs: can be 'rh=' (relative humidity in %), 'aw=' (vapor
    activity = rh / 100), 'p=' (partial water vapor pressure).

    Output
    ------
    Dewpoint Temperature in the same unit as the input temperature.
    """

    try:
        val, = humidity.values()  # check there is only one input humidity arg.
    except ValueError:
        raise ValueError("Humidity argument can only be 'p=', 'rh=' or 'aw='")

    if 'p' in humidity:
        p = val
    elif 'rh' in humidity:
        p = val / 100 * vapor_pressure(T, unit, source)
    elif 'aw' in humidity:
        p = val * vapor_pressure(T, unit, source)

    def psat(T):
        return vapor_pressure(T, unit, source)

    lower_T = 0 if unit == 'C' else 273.15
    dewpoint_calc = inversefunc(psat, domain=[lower_T, T])

    try:
        dpt = dewpoint_calc(p)
        return format_inverse_result(dpt)
    except ValueError:
        print(f"Error, probably because dewpoint less than 0°C or p>psat.")
        return None
