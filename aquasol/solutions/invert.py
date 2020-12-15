"""Inverse functions for solutions"""

# Non standard imports
from pynverse import inversefunc

# local imports
from .general import get_infos
from .properties import water_activity
from .convert import convert

from ..format import format_source, format_output_type


# ======================== ACTIVITY TO CONCENTRATION =========================


def aw_to_conc(a, out='w', solute='NaCl', T=25, unit='C', source=None):
    """Calculate concentration needed to achieve a certain water activity.

    Parameters
    ----------
    - a is the water activity,
    - out: any concentration unit manageable by convert()
    - solute (default NaCl) is the solute of interest
    - T: temperature
    - unit: temperature unit ('C' or 'K')
    - source: if None, use default source.

    Output
    ------
    Concentration using the units asked for with the "out" parameter.

    Examples
    --------
    aw_to_conc(0.39)
    >>> 0.4902761745068064  # in terms of weight fraction
    aw_to_conc([0.39, 0.75], out='m')
    >>> array([16.45785963,  6.21127029])  # in terms of molality
    aw_to_conc(0.11, 'r', 'LiCl', T=50)
    >>> 0.9167650291014361  # in terms of mass ratio, for LiCl, at 50°C

    Note: part of the structure of this function resembles that of
    general.calculation(), so see if there is a way to avoid redundancy
    """

    # Find infos on souces for the property of interest
    infos = get_infos('water activity', solute)

    # Check range of allowed concentrations in source ------------------------
    src = format_source(source, infos['sources'], infos['default source'])
    cunit = infos['conc units'][src]
    cmin, cmax = infos['conc ranges'][src]

    def activity(conc):
        cinfo = {cunit: conc}
        return water_activity(solute, T, unit, src, **cinfo)

    concentration = inversefunc(activity, domain=[cmin, cmax])

    try:
        conc = concentration(a)
    except ValueError:
        print(f"{a} outside of range of validity of {src}'s' formula")
        return None
    else:
        c = convert(conc, cunit, out, solute, T, unit)
        return format_output_type(c)
