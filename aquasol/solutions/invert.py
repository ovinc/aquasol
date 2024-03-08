"""Inverse functions for solutions"""

# Non standard imports
from pynverse import inversefunc

# local imports
# (DO NOT import from . because it will create circular import problems)
from .properties import water_activity
from .convert import convert

from ..format import format_output_type


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
    formula = water_activity.get_formula(solute=solute, source=source)
    cunit = formula.concentration_unit
    cmin, cmax = formula.concentration_range

    def activity(conc):
        return water_activity(
            solute=solute,
            T=T,
            unit=unit,
            source=source,
            **{cunit: conc},
        )

    concentration = inversefunc(activity, domain=[cmin, cmax])

    try:
        conc = concentration(a)
    except ValueError:
        src = water_activity.get_source(solute=solute, source=source)
        print(f"{a} outside of range of validity of {src}'s' formula")
        return None
    else:
        c = convert(
            value=conc,
            unit1=cunit,
            unit2=out,
            solute=solute,
            T=T,
            unit=unit,
        )
        return format_output_type(c)
