"""Miscellaneous checks for the thermo-ov package."""


from warnings import warn
import numpy as np


# ============================= GENERIC FUNCTIONS ============================

def check_units(units, allowed_units):
    """Check if units are among the allowed units to use, raise exception if not."""
    wrong_units = []
    for unit in units:
        if unit not in allowed_units:
            wrong_units.append(unit)
    if len(wrong_units) > 0:
        raise ValueError(f'{wrong_units} not in allowed units {allowed_units}')

def check_validity_range(value, okrange, dataname='', unitname='', sourcename=''):
    """Manage sources and associated validity range.

    Check that value is in validity range, and issues warning (no error) if not.

    Parameters
    ----------

    Obligatory:
    - value (scalar, list, array, tuple etc.), in the same unit as okrange.
    - okrange: (tuple (min, max)), same unit as value.

    Optional (used only for the warning to be explicit):
    - dataname (str): name of the parameter (e.g. 'temperature'),
    - unitname (str): unit of the source data (e.g. '°C' or 'x')
    - sourcename (str): name of the source of the data

    """

    try:  # This works only if value is a single value, not an array or a list
        test = value < okrange[0] or value > okrange[1]
    except ValueError:  # if array, list, array, tuple etc, transform to 1D np array
        values = np.array(value).flatten()
        test = any(values < okrange[0]) or any(values > okrange[1])

    if test:
        warn(f'{dataname} outside of validity range ({unitname} in {okrange}) '
             f'for {sourcename}.', stacklevel=2)


# ========================== FUNCTIONS for SOLUTIONS =========================

def check_solute(solute, allowed_solutes):
    """Check if solute in allowed solutes to use, raise exception if not"""
    if solute not in allowed_solutes:
        raise ValueError(f"{solute} not in allowed solutes: {allowed_solutes}")
