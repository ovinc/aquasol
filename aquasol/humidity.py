"""Miscellaneous formatting tools for humidity

(NOT WITH format module due to circular import problems)
"""

import numpy as np

from .water import vapor_pressure


# ================================== Config ==================================

hparams = ['p', 'rh', 'aw']

hratio = {'rh': 1 / 100, 'aw': 1}  # factor to go from humidity to activity
msg_humidity_error = "Humidity argument can only be 'p=', 'rh=' or 'aw='"

# ============================================================================


def format_humidity(unit='C', T=25, source=None, out='p', **humidity):
    """Manage conversion between p=, rh= and aw= keywordsil.

    Parameters
    ----------
    - unit: temperature unit ('C' or 'K')
    - T: temperature, required only if rh or aw are used (optional for p)
    - source: literature source for the calculation (if None --> default)
    - out: output parameter ('p', 'rh' or 'aw')
    - humidity kwargs: can be 'rh=' (relative humidity in %), 'aw=' (vapor
    activity = rh / 100), 'p=' (partial water vapor pressure).

    Output
    ------
    p (partial vapor pressure in Pa, float), rh, or aw depending on 'out'.

    Note: cannot be in the aquasol.format module because it needs to import
    vapor_pressure, which causes circular imports problems.
    """
    try:
        hin, = humidity.keys()    # humidity keyword
        val, = humidity.values()  # check there is only one input humidity arg.
    except ValueError:
        raise KeyError(msg_humidity_error)

    if hin not in hparams:
        raise KeyError(msg_humidity_error)

    if out in hparams:
        hout = out
    else:
        raise ValueError(f'out parameter can only be in {hparams}')

    if hin == hout:
        return val

    elif 'p' in [hin, hout]:
        # need to convert to/from p to aw/rh --> need psat(T)
        if T is None:
            T = 25 if unit == 'C' else 298.15  # 25°C is default T for RH, aw

        psat = vapor_pressure(
            T=T,
            unit=unit,
            source=source,
        )

        if hin == 'p':
            return np.array(val) / (psat * hratio[hout])
        else:  # p is not the input but the output
            return np.array(val) * (psat * hratio[hin])

    else:  # just a conversion between aw and rh
        return np.array(val) * hratio[hin] / hratio[hout]
