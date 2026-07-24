"""Miscellaneous formatting tools for humidity.

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
    """Manage conversion between p=, rh=, and aw= keywords.

    Parameters
    ----------
    unit : str, optional
        Temperature unit ('C' or 'K'). Default is 'C'.
    T : float, optional
        Temperature, required only if `rh` or `aw` are used (optional for `p`).
        Default is 25.
    source : str, optional
        Literature source for the calculation. If None, the default is used.
    out : str, optional
        Output parameter ('p', 'rh', or 'aw'). Default is 'p'.
    **humidity : kwargs
        Humidity input as one of the following:
        - `rh`: relative humidity in %.
        - `aw`: vapor activity (rh / 100).
        - `p`: partial water vapor pressure.

    Returns
    -------
    float or array-like
        Partial vapor pressure in Pa, relative humidity, or water activity,
        depending on the `out` parameter.

    Notes
    -----
    Cannot be in the aquasol.format module because it needs to import
    vapor_pressure, which causes circular import problems.
    """
    try:
        hin, = humidity.keys()  # humidity keyword
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
