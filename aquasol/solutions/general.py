"""Global management of modules and formulas for solutions."""


# TODO: write available_solutes function that returns a list of solutes available for a given property


from ..format import format_temperature, format_concentration, format_source
from ..check import check_validity_range


# Info on the name of the modules corresponding to the properties ------------

base = '.formulas.'
property_modules = {'water activity': base + 'activity',
                    'density': base + 'density',
                    'surface tension': base + 'surface_tension'}


def get_infos(propty, solute):
    """Get various informations on sources for a particular property and solute.

    Inputquit()
    -----
    propty (str): property name (e.g. 'water activity', 'density')
    solute (str): solute name (e.g. 'NaCl')

    Output
    ------
    Dictionary of informations, with the keys: 'sources', 'default source',
    'formulas', 'temp ranges', 'temp units', 'conc ranges', 'conc units'

    """

    module = property_modules[propty] + '.' + solute

    line1 = f'from {module} import concentration_types, concentration_ranges'
    line2 = f'from {module} import temperature_ranges, temperature_units'
    line3 = f'from {module} import sources, formulas, default_source'

    for line in line1, line2, line3:
        try:
            exec(line, globals())  # without globals, variables are not defined
        except ModuleNotFoundError:
            raise ModuleNotFoundError(f'solute {solute} not available')

    infos = {'sources': sources,
             'default source': default_source,
             'formulas': formulas,
             'temp ranges': temperature_ranges,
             'temp units': temperature_units,
             'conc ranges': concentration_ranges,
             'conc units': concentration_types}

    return infos


def calculation(propty, solute, source, parameters, converter):
    """Choose a formula for a solute, given a source and a list of modules.

    Inputs
    ------
    propty (str): property name (e.g. 'water activity', 'density')
    solute (str): solute name (e.g. 'NaCl')
    source (str): source name (if None, uses default source in module)
    parameters: tuple (T, unit, concentration)
    converter: concentration conversion function (convert or basic_convert)

    Output
    ------
    solute property of interest calculated following the parameters
    """

    T, unit, concentration = parameters

    # Find infos on souces for the property of interest
    infos = get_infos(propty, solute)

    # Set adequate source (default, or asked by user)
    src = format_source(source, infos['sources'], infos['default source'])

    # Check and format temperature -------------------------------------------
    tunit = infos['temp units'][src]
    trange = infos['temp ranges'][src]

    T = format_temperature(T, unit, tunit)
    check_validity_range(T, trange, 'temperature', tunit, src)

    # Check and format concentration -----------------------------------------

    cunit = infos['conc units'][src]
    crange = infos['conc ranges'][src]

    conc = format_concentration(concentration, cunit, solute, converter)
    check_validity_range(conc, crange, 'concentration', cunit, src)

    # Calculate value according to adequate formula --------------------------

    formula = infos['formulas'][src]
    return formula(conc, T)