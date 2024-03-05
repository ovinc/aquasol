"""Invert some properties for water (e.g., dewpoint from vapor_pressure)."""

# Non-standard imports
from pynverse import inversefunc

# Local imports
from .properties import vapor_pressure
from .general import get_infos

from ..format import format_temperature, format_source, format_output_type
from ..humidity import format_humidity


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

    Examples
    --------
    >>> dewpoint(p=1000)  # Dew point of a vapor at 1kPa
    6.970481357025221
    >>> dewpoint(p=1000, unit='K')  # Same, but temperature is returned in K
    280.1204813570252
    >>> dewpoint('K', p=1000)  # same thing
    280.1204813570252
    >>> dewpoint(rh=50)  # Dew point at 50%RH and 25°C (default)
    13.864985413550704
    >>> dewpoint(aw=0.5)  # same thing
    13.864985413550704
    >>> dewpoint(aw=0.5, T=20)  # same thing, but at 20°C
    9.273546905501904
    >>> dewpoint('K', 300, aw=0.5)  # same thing, but at 300K (dewpoint also in K)
    288.71154892380787
    >>> dewpoint(aw=[0.5, 0.7])  # It is possible to input lists, tuples, arrays
    array([ 9.27354606, 14.36765209])
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
        msg = "Error, probably because T outside of Psat formula validity range"
        raise ValueError(msg)
