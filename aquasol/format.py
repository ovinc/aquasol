"""Miscellaneous formatting tools and checks for the aquasol package."""

import functools

import numpy as np


def check_units(units, allowed_units):
    """Check if units are among allowed units, raise exception if not.

    Parameters
    ----------
    units : list
        Units to check.
    allowed_units : list
        Allowed units for validation.

    Raises
    ------
    ValueError
        If any unit in `units` is not in `allowed_units`.
    """
    wrong_units = []
    for unit in units:
        if unit not in allowed_units:
            wrong_units.append(unit)
    if len(wrong_units) > 0:
        raise ValueError(f'{wrong_units} not in allowed units {allowed_units}')


def format_input_type(value):
    """If type of input doesn't support math operations, convert to np array.

    Parameters
    ----------
    value : any
        Input value to check and potentially convert.

    Returns
    -------
    any
        Converted value as a numpy array if necessary, otherwise unchanged.
    """
    try:
        value + 1
    except TypeError:
        return np.array(value)
    else:
        return value


def format_output_type(value):
    """Format the output of inverse functions the same way as the inputs.

    This is because e.g. pynverse outputs an array, but sometimes we want it
    to output a scalar if a scalar was put in.

    Parameters
    ----------
    value : any
        Input value to format.

    Returns
    -------
    any
        Scalar or array, depending on input type.
    """
    try:
        sh = value.shape
    except AttributeError:
        return value  # if not an array, it's a float, so return it right away
    else:
        if len(sh) == 0:  # this is to return a scalar if a scalar is used as input
            return value.item()
        else:
            return value


def format_temperature(T, unit_in, unit_out):
    """Format temperature from/to Celsius (C) and Kelvin (K).

    Parameters
    ----------
    T : int, float, or array-like
        Temperature value(s) to convert.
    unit_in : str
        Input temperature unit ('C' or 'K').
    unit_out : str
        Output temperature unit ('C' or 'K').

    Returns
    -------
    numpy.ndarray or float
        Converted temperature value(s).
    """
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


def format_concentration(concentration, unit_out, solute, converter, density_source):
    """Check if concentration unit is valid and convert it to the desired unit.

    Parameters
    ----------
    concentration : dict
        Dictionary from main function **kwargs (e.g., {'w': 0.1}).
    unit_out : str
        The unit to format the value into (e.g., 'w').
    solute : str
        Name of the solute (e.g., 'NaCl').
    converter : callable
        Concentration conversion function (e.g., `convert` or `basic_convert`).
    density_source : str or None
        Source for density in case concentration or `unit_out` involves molarities.

    Returns
    -------
    any
        Value in the `unit_out` unit.

    Notes
    -----
    Checking if concentration is in the right unit and transforming into
    array if input is tuple, list, etc., is done by the converter.
    """
    if len(concentration) > 1:
        raise ValueError('concentration must have a single keyword argument')

    if len(concentration) == 0:
        raise ValueError(f'Concentration of {solute} not provided.')

    (unit_in, value), = concentration.items()

    kwargs = {'value': value, 'unit1': unit_in, 'unit2': unit_out, 'solute': solute}

    try:
        conc = converter(**kwargs, density_source=density_source)
    except TypeError:  # if converter is basic_convert, does not accept density_source as argument
        conc = converter(**kwargs)

    return conc


def make_array(function):
    """Decorator to execute function on arrays even if not designed to accept arrays.

    Parameters
    ----------
    function : callable
        Function to decorate.

    Returns
    -------
    callable
        Wrapped function that handles arrays.
    """
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
    """Decorator to execute method on arrays even if not designed to accept arrays.

    Parameters
    ----------
    method : callable
        Method to decorate.

    Returns
    -------
    callable
        Wrapped method that handles arrays.
    """
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


def make_array_args(function):
    """Decorator to execute function on arrays even if not designed to accept arrays.

    This one looks for an iterable in args, not in kwargs.
    Any position of the arg can be iterable, the first one will be chosen if several.

    Parameters
    ----------
    function : callable
        Function to decorate.

    Returns
    -------
    callable
        Wrapped function that handles arrays in positional arguments.
    """
    @functools.wraps(function)  # to preserve function signature
    def wrapper(*args, **kwargs):

        for i, val in enumerate(args):
            try:
                iter(val)
            except TypeError:  # Not an array --> continue searching
                pass
            else:
                iter_index = i
                iter_val = val
                break
        else:  # No iterable has been found --> apply function directly
            return function(*args, **kwargs)

        result = []

        for val in iter_val:
            new_args = list(args)
            new_args[iter_index] = val
            y = function(*new_args, **kwargs)
            result.append(y)

        return np.array(result)

    return wrapper


def make_array_kwargs(function):
    """Decorator to execute function on arrays even if not designed to accept arrays.

    Here, the array/iterable needs to be passed in the kwargs.
    Any kwargs will work, no matter the order.
    If there are several kwargs with iterables, only the first one will be considered.

    Parameters
    ----------
    function : callable
        Function to decorate.

    Returns
    -------
    callable
        Wrapped function that handles arrays in keyword arguments.
    """
    @functools.wraps(function)  # to preserve function signature
    def wrapper(*args, **kwargs):

        for key, val in kwargs.items():
            try:
                iter(val)
            except TypeError:  # Not an array --> continue searching
                pass
            else:
                iter_key = key
                iter_val = kwargs.pop(key)  # Array: store it elsewhere
                break
        else:  # No iterable has been found --> apply function directly
            return function(*args, **kwargs)

        result = []

        for val in iter_val:
            new_kwargs = {iter_key: val, **kwargs}
            y = function(*args, **new_kwargs)
            result.append(y)

        return np.array(result)

    return wrapper
