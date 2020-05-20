"""Global management of modules and formulas for water."""


from ..format import format_temperature, format_source
from ..check import check_validity_range


# Info on the name of the modules corresponding to the properties ------------

base = '.formulas.'
property_modules = {'vapor pressure': base + 'vapor_pressure',
                    'surface tension': base + 'surface_tension',
                    'density saturated': base + 'density_sat',
                    'density ambient': base + 'density_atm'}



def get_infos(propty):
    """Get various informations on sources for a particular property.

    Input
    -----
    propty (str): property name (e.g. 'vapor pressure', 'surface tension')

    Output
    ------
    Dictionary of informations, with the following keys:
    'sources', 'default source', 'formulas', 'temp ranges', 'temp units'

    """

    module = property_modules[propty]

    line1 = f'from {module} import temperature_ranges, temperature_units'
    line2 = f'from {module} import sources, formulas, default_source'

    for line in line1, line2:
        exec(line, globals())  # without globals, variables are not defined

    infos = {'sources': sources,
             'default source': default_source,
             'formulas': formulas,
             'temp ranges': temperature_ranges,
             'temp units': temperature_units}

    return infos


def calculation(propty, source, parameters):
    """Choose water property formula, given a source and a list of modules.

    Inputs
    ------
    propty (str): property name (e.g. 'vapor pressure', 'surface tension')
    source (str): source name (if None, uses default source in module)
    T: temperature
    unit (str): unit of temperature ('C' or 'K')

    Output
    ------
    water property of interest calculated following the input parameters
    """

    T, unit = parameters

    # Find infos on souces for the property of interest
    infos = get_infos(propty)

    # Set adequate source (default, or asked by user)
    src = format_source(source, infos['sources'], infos['default source'])

    # Check and format temperature -------------------------------------------
    tunit = infos['temp units'][src]
    trange = infos['temp ranges'][src]

    T = format_temperature(T, unit, tunit)
    check_validity_range(T, trange, 'temperature', tunit, src)

    # Calculate value according to adequate formula --------------------------

    formula = infos['formulas'][src]
    return formula(T)
