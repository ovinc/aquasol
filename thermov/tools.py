"""Miscellaneous tools for the thermo-ov package."""


from .solutions.conversions_basic import convert
from .checks import check_validity_range


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


def format_concentration(concentration, unit_out, solute):
    """Check if concentration unit is ok and convert it to the unit_out unit.

    Parameters
    ----------
    concentration: dict from main function **kwargs (e.g. {'w': 0.1})
    out_unit: the unit to format the value into (e.g. 'w')
    solute: name of the solute (e.g. 'NaCl')
    kwargs: must be in the form 'w=value'

    Output
    ------
    value in the unit_out unit
    """
    if len(concentration) > 1:
        raise ValueError('concentration must have a single keyword argument')
    if len(concentration) == 0:
        raise ValueError(f'Concentration of {solute} not provided.')
    else:
        [unit_in] = concentration.keys()
        [value] = concentration.values()
        conc = convert(value, unit_in, unit_out, solute)
        return conc


# ==================== IMPORTING MODULES AND FORMULAS ========================

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



def solution_calculation(solute, source, modules, parameters):
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

    conc = format_concentration(concentration, cunit, solute)
    check_validity_range(conc, crange, 'concentration', cunit, src)

    # Calculate value according to adequate formula --------------------------

    formula = formulas[src]
    return formula(conc, T)

