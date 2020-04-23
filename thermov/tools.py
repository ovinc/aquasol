"""Miscellaneous tools for the thermo-ov package."""


from .solutions.conversions_basic import convert


# ============================ MISC. FORMATTING ==============================

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

    for unit in [unit_in, unit_out]:
        if unit not in allowed_units:
            raise ValueError(f'{unit} is not a valid temperature unit (C or K)')

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


def format_concentration(kwargs, unit_out, solute):
    """Check if concentration unit is ok and convert it to the unit_out unit.

    Parameters
    ----------
    kwargs: dictionary got from main function **kwargs (should be e.g. {'w': 0.1})
    out_unit: the unit to format the value into (e.g. 'w')
    solute: name of the solute (e.g. 'NaCl')
    kwargs: must be in the form 'w=value'

    Output
    ------
    value in the unit_out unit
    """
    if len(kwargs) > 1:
        raise ValueError('kwargs must have a single keyword argument for solute concentration')
    if len(kwargs) == 0:
        raise ValueError(f'Concentration of {solute} not provided.')
    else:
        [unit_in] = kwargs.keys()
        [value] = kwargs.values()  # corresponding value in the unit above
        val = convert(value, unit_in, unit_out, solute)
        return val


# =========================== IMPORTING MODULES ==============================

def import_solute_module(modules, solute, sourcename):
    """Import module corresponding to solute data."""

    try:
        module = modules[solute]
    except KeyError:
        allowed_solutes = list(modules.keys())
        raise ValueError(f'Solute can only be one of {allowed_solutes}')

    line1 = f'from .solutions.{module} import concentration_types, concentration_ranges'
    line2 = f'from .solutions.{module} import temperature_ranges, temperature_units'
    line3 = f'from .solutions.{module} import sources, formulas, default_source'

    for line in line1, line2, line3:
        exec(line, globals())  # without globals, variables are not defined

    source = format_source(sourcename, sources, default_source)

    data = (source, formulas,
            concentration_types, concentration_ranges,
            temperature_units, temperature_ranges)

    return data

