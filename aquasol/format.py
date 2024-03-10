"""Miscellaneous formatting tools and checks for the aquasol package."""

import functools

import numpy as np


def check_units(units, allowed_units):
    """Check if units are among allowed units, raise exception if not."""
    wrong_units = []
    for unit in units:
        if unit not in allowed_units:
            wrong_units.append(unit)
    if len(wrong_units) > 0:
        raise ValueError(f'{wrong_units} not in allowed units {allowed_units}')


def check_solute(solute, allowed_solutes):
    """Check if solute in allowed solutes to use, raise exception if not"""
    if solute not in allowed_solutes:
        raise ValueError(f"{solute} not in allowed solutes: {allowed_solutes}")


def format_input_type(value):
    """If type of input doesn't support math operations, convert to np array."""
    try:
        value + 1
    except TypeError:
        return np.array(value)
    else:
        return value


def format_output_type(value):
    """Formats the output of inverse functions the same way as the inputs.

    This is because e.g. pynverse outputs an array, but sometimes we want it
    to output a scalar if a scalar was put in.
    """
    try:
        sh = value.shape
    except AttributeError:
        return value   # if not an array, it's a float, so return it rightaway
    else:
        if len(sh) == 0:  # this is to return a scalar if a scalar is used as input
            return value.item()
        else:
            return value


def format_temperature(T, unit_in, unit_out):
    """Format temperature from/to Celsius (C) and Kelvin (K)."""

    allowed_units = 'C', 'K'
    check_units([unit_in, unit_out], allowed_units)

    T = format_input_type(T)  # allows for lists and tuples as inputs

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

    (unit_in, value), = concentration.items()

    conc = converter(value=value, unit1=unit_in, unit2=unit_out, solute=solute)
    return conc


def make_array(function):
    """Decorator to execute function on arrays even when it's not designed initially to accept arrays"""

    @functools.wraps(function)  # to preserve function signature
    def wrapper(x, *args, **kwargs):
        try:
            iter(x)
        except TypeError:  # Not an array
            return function(x, *args, **kwargs)
        else:
            result = []
            for xi in x:
                y = function(xi, *args, **kwargs)
                result.append(y)
            return np.array(result)
    return wrapper


def make_array_method(method):
    """Decorator to execute method on arrays even when it's not designed initially to accept arrays"""

    @functools.wraps(method)  # to preserve method signature
    def wrapper(self, x, *args, **kwargs):
        try:
            iter(x)
        except TypeError:  # Not an array
            return method(self, x, *args, **kwargs)
        else:
            result = []
            for xi in x:
                y = method(self, xi, *args, **kwargs)
                result.append(y)
            return np.array(result)
    return wrapper