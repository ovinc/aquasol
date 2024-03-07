"""Invert some properties for water (e.g., dewpoint from vapor_pressure)."""

# Non-standard imports
from pynverse import inversefunc

# Local imports
from . import vapor_pressure

from ..format import format_temperature, format_output_type
from ..humidity import format_humidity


def dewpoint(unit='C', T=None, source=None, **humidity):
    """Inverts vapor_pressure() to calculate dew point at a given humidity.

    Inputs
    ------
    - unit: temperature unit of dewpoint, can be 'C' or 'K' (default 'C')
    - T: system temperature, required only if rh or aw are used as humidity
    input value, but optional if p is used. Default None, i.e 25°C.
    - source: literature source for the calculation of vapor pressure
              (default: None, i.e. Auto); see water.vapor_pressure
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
    p = format_humidity(
        unit=unit,
        T=T,
        source=source,
        out='p',
        **humidity,
    )
    source = vapor_pressure.get_source(source=source)
    trange_source = vapor_pressure.formulas[source].temperature_range
    tunit_source = vapor_pressure.formulas[source].temperature_unit

    # invert vapor pressure function to get dewpoint -------------------------

    def psat(Ts):
        return vapor_pressure(Ts, unit=tunit_source, source=source)

    dewpoint_calc = inversefunc(psat, domain=trange_source)

    try:
        dpt = dewpoint_calc(p)
        T_out = format_temperature(T=dpt, unit_in=tunit_source, unit_out=unit)
        return format_output_type(T_out)

    except ValueError:
        msg = "Error, probably because T outside of Psat formula validity range"
        raise ValueError(msg)
