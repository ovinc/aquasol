"""Inverse functions for solutions"""

# Non standard imports
from pynverse import inversefunc

# local imports
from .general import get_infos
from .properties import water_activity
from .convert import convert

from ..format import format_source, format_inverse_result


# ======================== ACTIVITY TO CONCENTRATION =========================


def aw_to_conc(a, out='w', solute='NaCl', T=25, unit='C', source=None):
    """Calculate concentration needed to achieve a certain water activity.

    - a is the water activity,
    - out: any concentration unit manageable by convert()
    - solute (default NaCl) is the solute of interest
    - T: temperature
    - unit: temperature unit ('C' or 'K')
    - source: if None, use default source.

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
        return format_inverse_result(c)
