"""Misc. checks. Separated from tools.py to avoid circular imports"""


from warnings import warn
import numpy as np

def check_solute(solute, allowed_solutes):
    """Check if solute in allowed solutes to use, raise exception if not"""
    if solute not in allowed_solutes:
        raise ValueError(f"{solute} not in allowed solutes: {allowed_solutes}")


def check_units(units, allowed_units):
    """Check if units are among the allowed units to use, raise exception if not."""
    wrong_units = []
    for unit in units:
        if unit not in allowed_units:
            wrong_units.append(unit)
    if len(wrong_units) > 0:
        raise ValueError(f'{wrong_units} not in allowed units {allowed_units}')

def check_validity_range(value, source, source_units, source_ranges, dataname):
    """Manage sources and associated validity range.

    Check that value is in validity range, and issues warning (no error) if not.

    Parameters
    ----------
    - value: must be in the same unit as the okrange.
    - source is the name of the data source.
    - source_unit: unit of the source data (e.g. '°C' or 'x', used only for the
    warning to be explicit.
    - source_ranges: must be in the form of a dictionary of tuples (min, max) with
    the source name as a key.
    - dataname is the name of the parameter (e.g. 'temperature'), this is used
    only for the warning to be explicit.
    """
    unit = source_units[source]
    okrange = source_ranges[source]

    try:  # This works only if value is a single value, not an array or a list
        test = value < okrange[0] or value > okrange[1]
    except ValueError:  # if array, list, array, tuple etc, transform to 1D np array
        values = np.array(value).flatten()
        test = any(values < okrange[0]) or any(values > okrange[1])

    if test:
        warn(f'{dataname} outside of validity range ({unit} in {okrange}) '
             f'for {source}.', stacklevel=2)

