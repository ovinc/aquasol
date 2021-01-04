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
rpparams = ['r', 'P']

hratio = {'rh': 1 / 100, 'aw': 1}  # factor to go from humidity to activity
msg_humidity_error = "Humidity argument can only be 'p=', 'rh=' or 'aw='"
msg_rp_error = "Input argument can only be 'r=' (radius in m) or 'P='" \
               "(liquid pressure in Pa)"


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


# ============== Humidity to kelvin radius and inverse function ==============


def kelvin_pressure(T=25, unit='C', **humidity):
    """Calculate Kelvin (liquid) pressure at a given humidity.

    Parameters
    ----------
    - T: temperature (default 25)
    - unit: temperature unit ('C' or 'K', default 'C')
    - humidity: kwargs p=, rh= or aw=

    Output
    ------
    Kelvin pressure in Pa.

    Examples
    --------
    >>> kelvin_pressure(aw=0.8)  # Kelvin pressure at 80%RH and T=25°C
    -30613102.83763792
    >>> kelvin_pressure(rh=80)           # same
    -30613102.83763792
    >>> kelvin_pressure(p=1000, T=20)    # at 1000Pa, 20°C
    -114763155.07026532
    >>> kelvin_pressure(p=1000, T=293.15, unit='K')    # same
    -114763155.07026532
    >>> kelvin_pressure(aw=[0.5, 0.7, 0.9])  # possible to use iterables
    array([-95092982.94809894, -48932297.94944938, -14454427.57302842])
    """
    aw = format_humidity(unit, T, out='aw', **humidity)
    vm = Mw / density_sat(T, unit)
    Tk = format_temperature(T, unit, 'K')
    pc = R * Tk * np.log(aw) / vm  # no need to use format_input_type due to np.log
    return format_output_type(pc)


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

    Examples
    --------
    >>> kelvin_radius(aw=0.8)  # Kelvin radius at 80%RH and T=25°C
    4.702052295185309e-09
    >>> kelvin_radius(rh=80)           # same
    4.702052295185309e-09
    >>> kelvin_radius(rh=80, ncurv=1)  # assume cylindrical meniscus instead of spherical
    2.3510261475926545e-09
    >>> kelvin_radius(p=1000, T=20)    # at 1000Pa, 20°C
    1.2675869773199224e-09
    >>> kelvin_radius(p=1000, T=293.15, unit='K')    # same
    1.2675869773199224e-09
    >>> kelvin_radius(aw=[0.5, 0.7, 0.9])  # possible to use iterables
    array([1.51372274e-09, 2.94170551e-09, 9.95849955e-09])
    """
    sig = surface_tension(T, unit)
    pc = kelvin_pressure(T=T, unit=unit, **humidity)
    r = -ncurv * sig / pc
    return format_output_type(r)


def kelvin_humidity(T=25, unit='C', ncurv=2, out='aw', **r_or_p):
    """Calculate humidity corresponding to a Kelvin radius.

    Parameters
    ----------
    - r: Kelvin radius in meters
    - T: temperature (default 25)
    - unit: temperature unit ('C' or 'K', default 'C')
    - ncurv: curvature number: 1 cylindrical interface, 2 spherical (default)
    - out: type of output ('p', 'rh', or 'aw')
    - input: kwargs (r= for radius, or p= for liquid pressure)

    Output
    ------
    Kelvin radius in meters.

    Examples
    --------
    # With radius in meters as input -----------------------------------------
    >>> kelvin_humidity(r=4.7e-9)  # activity corresponding to Kelvin radius of 4.7 nm at 25°C
    0.7999220537658477
    >>> kelvin_humidity(r=4.7e-9, out='rh')  # same, but expressed in %RH instead of activity
    79.99220537658476
    >>> kelvin_humidity(r=4.7e-9, out='p')  # same, but in terms of pressure (Pa)
    2535.612513169546
    >>> kelvin_humidity(r=4.7e-9, out='p', T=293.15, unit='K')  # at a different temperature
    1860.0699544036922
    >>> kelvin_humidity(r=4.7e-9, ncurv=1)  # cylindrical interface
    0.8943836166689592
    >>> kelvin_humidity(r=[3e-9, 5e-9])  # with iterables
    array([0.70486836, 0.81070866])

    # Similar examples, but with liquid pressure (Pa) as input ---------------
    >>> kelvin_humidity(P=-30e6)  # humidity corresponding to P=-30 MPa
    0.8035832003814989
    >>> kelvin_humidity(P=-30e6, out='rh')
    80.35832003814988
    >>> kelvin_humidity(P=-30e6, out='p', T=293.15, unit='K')
    1873.2224722706874
    >>> kelvin_humidity(P=[-30e6, -50e6])
    array([0.8035832 , 0.69457329])
    """
    try:
        rpin, = r_or_p.keys()    # radius or pressure keyword
        val, = r_or_p.values()  # check there is only one input humidity arg.
    except ValueError:
        raise KeyError(msg_rp_error)

    if rpin not in rpparams:
        raise KeyError(msg_rp_error)

    if rpin == 'r':
        r = format_input_type(val)
        sig = surface_tension(T, unit)
        pc = - ncurv * sig / r
    else:
        pc = format_input_type(val)

    vm = Mw / density_sat(T, unit)
    Tk = format_temperature(T, unit, 'K')
    aw = np.exp(pc * vm / (R * Tk))
    hout = format_humidity(unit, T, source=None, out=out, aw=aw)
    return format_output_type(hout)
