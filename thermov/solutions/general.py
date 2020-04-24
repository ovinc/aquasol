"""Global management of modules and formulas for solutions.
"""

from ..format import format_temperature, format_concentration, format_source
from ..check import check_validity_range


def import_solute_module(modules, solute, sourcename):
    """Import module corresponding to solute data."""

    try:
        module = modules[solute]
    except KeyError:
        allowed_solutes = list(modules.keys())
        raise ValueError(f'Solute can only be one of {allowed_solutes}')

    line1 = f'from .{module} import concentration_types, concentration_ranges'
    line2 = f'from .{module} import temperature_ranges, temperature_units'
    line3 = f'from .{module} import sources, formulas, default_source'

    for line in line1, line2, line3:
        exec(line, globals())  # without globals, variables are not defined

    source = format_source(sourcename, sources, default_source)

    data = (source, formulas,
            concentration_types, concentration_ranges,
            temperature_units, temperature_ranges)

    return data


def solution_calculation(solute, source, modules, parameters, converter):
    """Choose a formula for a solute, given a source and a list of modules.

    Inputs
    ------
    solute (str): solute name (e.g. 'NaCl')
    source (str): source name (if None, uses default source in module)
    modules (dict): dict with solutes as keys and corresponding modules
    as values
    parameters: tuple (T, unit, concentration)

    Output
    ------
    solute property of interest calculated following the parameters
    """

    T, unit, concentration = parameters

    # Import adequate submodule for calculations -----------------------------

    params = import_solute_module(modules, solute, source)
    (src, formulas, cunits, cranges, tunits, tranges) = params

    # Check and format temperature -------------------------------------------

    tunit = tunits[src]
    trange = tranges[src]

    T = format_temperature(T, unit, tunit)
    check_validity_range(T, trange, 'temperature', tunit, src)

    # Check and format concentration -----------------------------------------

    cunit = cunits[src]
    crange = cranges[src]

    conc = format_concentration(concentration, cunit, solute, converter)
    check_validity_range(conc, crange, 'concentration', cunit, src)

    # Calculate value according to adequate formula --------------------------

    formula = formulas[src]
    return formula(conc, T)