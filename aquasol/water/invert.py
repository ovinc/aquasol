"""Convert/invert some properties for water."""

# Non-standard imports
import numpy as np
from pynverse import inversefunc

# Local imports
from .properties import vapor_pressure, surface_tension, density_sat
from .general import get_infos

from ..format import format_temperature, format_source
from ..format import format_output_type, format_input_type
from ..constants import R, Mw

# ================================== Config ==================================

hparams = ['p', 'rh', 'aw']

hratio = {'rh': 1/100, 'aw': 1}  # factor to go from humidity to activity
msg_humidity_error = "Humidity argument can only be 'p=', 'rh=' or 'aw='"


# ============================ Misc. Subroutines =============================


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
        val, = humidity.values()  # check there is only one input humidity arg.
        hin, = humidity.keys()    # humidity keyword
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
        psat = vapor_pressure(T, unit, source)

        if hin == 'p':
            return np.array(val) / (psat * hratio[hout])
        else:  # p is not the input but the output
            return np.array(val) * (psat * hratio[hin])

    else:  # just a conversion between aw and rh
        return np.array(val) * hratio[hin] / hratio[hout]


# ============================== Main Functions ==============================


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
    p = format_humidity(unit, T, source, out='p', **humidity)

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
        T_out = format_temperature(dpt, unit_source, unit)
        return format_output_type(T_out)

    except ValueError:
        msg = f"Error, probably because T outside of Psat formula validity range"
        raise ValueError(msg)


# ============== Humidity to kelvin radius and inverse function ==============


def kelvin_radius(T=25, unit='C', ncurv=2, **humidity):
    """Calculate Kelvin radius at a given humidity.

    Parameters
    ----------
    - T: temperature (default 25)
    - unit: temperature unit ('C' or 'K', default 'C')
    - ncurv: curvature number: 1 cylindrical interface, 2 spherical (default)
    - humidity: kwargs p=, rh= or aw=

    Output
    ------
    Kelvin radius in meters.
    """
    aw = format_humidity(unit, T, out='aw', **humidity)
    vm = Mw / density_sat(T, unit)
    sig = surface_tension(T, unit)
    Tk = format_temperature(T, unit, 'K')
    pc = R * Tk * np.log(aw) / vm  # no need to use format_input_type due to np.exp
    r = -ncurv * sig / pc
    return format_output_type(r)


def kelvin_humidity(r, T=25, unit='C', ncurv=2, out='aw'):
    """Calculate humidity corresponding to a Kelvin radius.

    Parameters
    ----------
    - r: Kelvin radius in meters
    - T: temperature (default 25)
    - unit: temperature unit ('C' or 'K', default 'C')
    - ncurv: curvature number: 1 cylindrical interface, 2 spherical (default)
    - out: type of output ('p', 'rh', or 'aw')

    Output
    ------
    Kelvin radius in meters.
    """
    r = format_input_type(r)
    vm = Mw / density_sat(T, unit)
    sig = surface_tension(T, unit)
    pc = - ncurv * sig / r
    Tk = format_temperature(T, unit, 'K')
    aw = np.exp(pc * vm / (R * Tk))
    hout = format_humidity(unit, T, source=None, out=out, aw=aw)
    return format_output_type(hout)
