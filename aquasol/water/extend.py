"""Extension of the properties module for useful shortcut functions

e.g.:
- Kelvin pressure instead of vapor pressure
- molar volume instead of density
etc.
"""

import numpy as np

from . import density_atm, density_sat, surface_tension
from ..format import format_output_type, format_temperature, format_input_type
from ..humidity import format_humidity
from ..constants import Mw, R


# ================================== Config ==================================

rpparams = ['r', 'P']

msg_rp_error = "Input argument can only be 'r=' (radius in m) or 'P='" \
               "(liquid pressure in Pa)"

# ============================================================================


density = {
    'sat': density_sat,
    'atm': density_atm,
}


def molar_volume(T=25, unit='C', source=None, condition='sat'):
    """Molar volume of water [m^3 / mol].

    Parameters
    ----------
    - T (int, float, array, list, tuple): temperature
    - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
    - source (str, default None) : Source for the used equation, if None then
    the default source for the particular property is used.
    - condition: 'sat' (default): sat. pressure, 'atm': at atm. pressure

    Output
    ------
    Molar volume in m^3 / mol

    Sources
    -------
    see density_atm() and density_sat()
    """
    return Mw / density[condition](T=T, unit=unit, source=source)


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
    aw = format_humidity(unit=unit, T=T, source=None, out='aw', **humidity)
    vm = molar_volume(T=T, unit=unit, source=None)
    Tk = format_temperature(T=T, unit_in=unit, unit_out='K')
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
    sig = surface_tension(T=T, unit=unit)
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
        sig = surface_tension(T=T, unit=unit)
        pc = - ncurv * sig / r
    else:
        pc = format_input_type(val)

    vm = molar_volume(T=T, unit=unit)
    Tk = format_temperature(T=T, unit_in=unit, unit_out='K')
    aw = np.exp(pc * vm / (R * Tk))
    hout = format_humidity(unit=unit, T=T, source=None, out=out, aw=aw)
    return format_output_type(hout)
