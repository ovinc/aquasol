"""Global management of modules and formulas for water."""


from ..format import format_temperature, format_source
from ..check import check_validity_range


def import_water_module(module, source):
    """Import module corresponding to water data."""

    line1 = f'from .{module} import temperature_ranges, temperature_units'
    line2 = f'from .{module} import sources, formulas, default_source'

    for line in line1, line2:
        exec(line, globals())  # without globals, variables are not defined

    src = format_source(source, sources, default_source)

    data = (src, formulas, temperature_units, temperature_ranges)

    return data


def water_calculation(source, module, T, unit):
    """Choose water property formula, given a source and a list of modules.

    Inputs
    ------
    source (str): source name (if None, uses default source in module)
    module (str): name of module containing the formulas
    T: temperature
    unit (str): unit of temperature ('C' or 'K')

    Output
    ------
    water property of interest calculated following the parameters
    """

    # Import adequate submodule for calculations -----------------------------

    params = import_water_module(module, source)
    (src, formulas, tunits, tranges) = params

    # Check and format temperature -------------------------------------------

    tunit = tunits[src]
    trange = tranges[src]

    T = format_temperature(T, unit, tunit)
    check_validity_range(T, trange, 'temperature', tunit, src)

    # Calculate value according to adequate formula --------------------------

    formula = formulas[src]
    return formula(T)
