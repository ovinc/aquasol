"""Global management of modules and formulas for water."""


from ..format import format_temperature, format_source
from ..check import check_validity_range



class WaterFormula:
    """Generic class for formulas for water properties as a function of T"""

    # To be defined in subclasses
    name = ''
    source_name = ''
    temperature_unit = None
    temperature_range = None


class WaterProperty:
    """Generic class for a property that can have various sources"""

    formulas = ()
    default_formula = None

    def __init__(self):
        self.available_formulas = {
            formula.name: formula for formula in self.formulas
        }

    def _get_formula(self, source=None):
    """Return source if it's in sources, default_source if None."""
    if source is None:
        return default_source
    else:
        if source not in sources:
            raise ValueError(f'Source can only be one of {sources}')
        else:
            return source


    def calculate(self, T, unit='C', source=None):
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
