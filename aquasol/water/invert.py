"""Convert/invert some properties for water"""

# Non-standard imports
import numpy as np
from pynverse import inversefunc

# Local imports
from .properties import vapor_pressure
from .general import get_infos

from ..format import format_temperature, format_source
from ..format import format_inverse_result, format_type


hratio = {'rh': 1/100, 'aw': 1}  # factor to go from humidity to activity
msg_humidity_error = "Humidity argument can only be 'p=', 'rh=' or 'aw='"


def dewpoint(unit='C', T=None, source=None, **humidity):
    """Inverts vapor_pressure() to calculate dew point at a given humidity.

    Inputs
    ------
    - unit: temperature unit of dewpoint, can be 'C' or 'K' (default 'C')
    - T: system temperature, required only if rh or aw are used as humidity
    input value, but optional if p is used. Default None, i.e 25°C.
    - source: literature source for the calculation (default: None, i.e. Auto)
    - humidity kwargs: can be 'rh=' (relative humidity in %), 'aw=' (vapor
    activity = rh / 100), 'p=' (partial water vapor pressure).

    Output
    ------
    Dewpoint Temperature
    """
    try:
        val, = humidity.values()  # check there is only one input humidity arg.
        hmd, = humidity.keys()    # humidity keyword
    except ValueError:
        raise KeyError(msg_humidity_error)

    if hmd == 'p':
        p = val
    elif hmd in ['aw', 'rh']:
        if T is None:
            T = 25 if unit == 'C' else 298.15  # 25°C is default T for RH, aw
        p = np.array(val) * hratio[hmd] * vapor_pressure(T, unit, source)
    else:
        raise KeyError(msg_humidity_error)

    # Get validity range of the source to invert function on this whole range
    infos = get_infos('vapor pressure')
    src = format_source(source, infos['sources'], infos['default source'])
    unit_source = infos['temp units'][src]
    trange = infos['temp ranges'][src]

    # invert vapor pressure function to get dewpoint -------------------------

    def psat(Ts):
        return vapor_pressure(Ts, unit_source, source)

    dewpoint_calc = inversefunc(psat, domain=trange)

    try:
        dpt = dewpoint_calc(p)
        Ts_out = format_inverse_result(dpt)
        T_out = format_temperature(Ts_out, unit_source, unit)
        return T_out

    except ValueError:
        msg = f"Error, probably because T outside of Psat formula validity range"
        raise ValueError(msg)
