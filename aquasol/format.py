"""Miscellaneous formatting tools for the thermo-ov package."""


import numpy as np

from .check import check_units


def format_type(value):
    """If type of input doesn't support math operations, convert to np array."""
    try:
        value + 1
    except TypeError:
        return np.array(value)
    else:
        return value


def format_source(source, sources, default_source):
    """Return source if it's in sources, default_source if None."""
    if source is None:
        return default_source
    else:
        if source not in sources:
            raise ValueError(f'Source can only be one of {sources}')
        else:
            return source


def format_temperature(T, unit_in, unit_out):
    """Format temperature from/to Celsius (C) and Kelvin (K)."""

    allowed_units = 'C', 'K'
    check_units([unit_in, unit_out], allowed_units)

    T = format_type(T)  # allows for lists and tuples as inputs

    if unit_in == 'C':
        T_celsius = T
        T_kelvin = T + 273.15
    else:
        T_celsius = T - 273.15
        T_kelvin = T

    if unit_out == 'C':
        return T_celsius
    else:
        return T_kelvin


def format_concentration(concentration, unit_out, solute, converter):
    """Check if concentration unit is ok and convert it to the unit_out unit.

    Parameters
    ----------
    concentration: dict from main function **kwargs (e.g. {'w': 0.1})
    unit_out: the unit to format the value into (e.g. 'w')
    solute: name of the solute (e.g. 'NaCl')
    converter: concentration conversion function (convert or basic_convert)

    Output
    ------
    value in the unit_out unit

    Note
    ----
    Checking if concentration is in the right unit etc. and transforming into
    array if input is tuple, list etc. is done by the converter
    """

    if len(concentration) > 1:
        raise ValueError('concentration must have a single keyword argument')

    if len(concentration) == 0:
        raise ValueError(f'Concentration of {solute} not provided.')

    else:
        [unit_in] = concentration.keys()
        [value] = concentration.values()
        conc = converter(value, unit_in, unit_out, solute)
        return conc


