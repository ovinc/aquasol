"""Global management of modules and formulas for water."""

from warnings import warn

import numpy as np

from .format import format_temperature, format_concentration
from .format import format_output_type
from .solutions import convert


# ================== Classes to describe specific formulas ===================


class Formula:
    """base class for formulas for water/solution properties"""

    # To be defined in subclasses
    name = ''
    input_types = ()
    default = False  # Change to True to select default source

    def _get_range_and_unit(self, input_type):
        if input_type not in self.input_types:
            raise ValueError(f'Input type {input_type} not in {self.input_types}')
        okrange = getattr(self, f'{input_type}_range')
        unit = getattr(self, f'{input_type}_unit')
        return {'range': okrange, 'unit': unit}

    def check_validity_range(self, input_type, value):
        """Check value is in validity range, issues warning (no error) if not.

        Parameters
        ----------
        - value_type: 'temperature' or 'concentration'
        - value (scalar, list, array, tuple etc.), in the same unit as okrange.

        Optional (used only for the warning to be explicit):
        - dataname (str): name of the parameter (e.g. 'temperature'),
        - unitname (str): unit of the source data (e.g. '°C' or 'x')
        - sourcename (str): name of the source of the data
        """
        validity_info = self._get_range_and_unit(input_type=input_type)
        val_min, val_max = validity_info['range']
        unit = validity_info['unit']

        try:  # This works only if value is a single value, not an array or a list
            out_of_range = value < val_min or value > val_max
        except ValueError:  # if array, list, array, tuple etc, transform to 1D np array
            values = np.array(value).flatten()
            out_of_range = any(values < val_min) or any(values > val_max)

        if out_of_range:
            warn(
                f'{input_type.capitalize()} outside of validity range'
                f'({unit} in [{val_min}-{val_max}]) for {self.source}.',
                stacklevel=2
            )

    def calculate(self, *args, **kwargs):
        """To define in subclasses"""
        pass


class WaterFormula(Formula):
    """Formulas for water properties as a function of T"""

    # To be defined in subclasses
    temperature_unit = None
    temperature_range = None

    # Do not change below
    input_types = 'temperature',


class SolutionFormula(Formula):
    """Formulas for solution properties as a function of T and composition"""

    # To be defined in subclasses --------------------------------------------

    solute = None

    # if True, formula returns val(c=0) and val(c) to allow for relative calculations
    with_water_reference = False

    temperature_unit = None
    temperature_range = None
    concentration_unit = None
    concentration_range = None

    # Do not change below ----------------------------------------------------

    input_types = 'temperature', 'concentration'


class SaturatedSolutionFormula(Formula):
    """Formulas for saturated solution properties (depend only on T)"""

    # To be defined in subclasses --------------------------------------------

    solute = None

    temperature_unit = None
    temperature_range = None

    # Do not change below ----------------------------------------------------

    input_types = 'temperature',


# ----------------------------------------------------------------------------
# === Classes to describe properties containing one or multiple  formulas ====
# ----------------------------------------------------------------------------


class Property:
    """Base class for properties of water or solutions (e.g. density)"""

    # Below, to define in subclasses
    Formulas = ()  # iterable of formulae available to calculate the property
    quantity = None
    unit = None

    def __repr__(self):
        return f'{self.quantity.capitalize()} {self.unit} (default: {self.default_source})'


class WaterProperty(Property):
    """Generic class for a property that can have various sources"""

    def __init__(self):

        self.formulas = {}  # dict source_name: formula object

        for Formula in self.Formulas:

            formula = Formula()
            source = formula.name
            self.formulas[source] = formula

            if formula.default:
                self.default_source = source

        self.sources = tuple(self.formulas)  # only the source names

    def __call__(self, T=25, unit='C', source=None):
        """Calculate water property as a function of temperature

        Parameters
        ----------
        - T (int, float, array, list, tuple): temperature
        - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
        - source (str, default None) : Source for the used equation, if None then
        the default source for the particular property is used.

        Output
        ------
        Value of property in SI units
        (float or array of floats depending on input)

        Attributes
        ----------
        .sources --- list of available sources
        .default_source --- source used if None provided
        .quantity --- type of physical quantity (e.g. 'surface tension')
        .unit --- unit of physical quantity (e.g. '[N/m]')
        """
        source = self._get_source(source)
        formula = self.formulas[source]

        T = format_temperature(
            T,
            unit_in=unit,
            unit_out=formula.temperature_unit,
        )

        formula.check_validity_range('temperature', value=T)
        result = formula.calculate(T)
        return format_output_type(result)

    def _get_source(self, source=None):
        """Return source if it's in sources, default_source if None."""
        if source is None:
            return self.default_source
        if source in self.sources:
            return source
        raise ValueError(f'Source can only be one of {self.sources}')


class SolutionProperty(Property):
    """Generic class for a property of solutions as a function of T/c"""

    # Change in subclasses if needed (e.g. if NaCl not available)
    default_solute = 'NaCl'

    def __init__(self):

        self.solutes = self._get_available_solutes()

        self.formulas = {solute: {} for solute in self.solutes}
        self.sources = {}
        self.default_sources = {}

        for Formula in self.Formulas:

            formula = Formula()
            source = formula.name
            solute = formula.solute

            self.formulas[solute][source] = formula

            if formula.default:
                self.default_sources[solute] = source

            # only the source names
            self.sources[solute] = tuple(self.formulas[solute])

    def _get_available_solutes(self):
        solutes = set()
        for Formula in self.Formulas:
            solutes.add(Formula.solute)
        return tuple(solutes)

    def __repr__(self):
        return f'{self.quantity.capitalize()} {self.unit} (solutes: {self.solutes})'

    def __call__(
        self,
        solute=None,
        T=25,
        unit='C',
        relative=False,
        source=None,
        **concentration,
    ):
        """Calculate solution property as a function of temperature and composition

        Parameters
        ----------
        - solute (str): solute name (if None, use default solute)
        - T (float): temperature (default 25)
        - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
        - relative (bool, default False): True to normalize with pure water at T.
          [ONLY available for some of the properties, e.g. surface tension]

        - source (str, default None) : Source for the used equation, if None then
        gets the default source for the particular solute (defined in submodules).
        See summary of available sources below.

        - **concentration: kwargs with any unit that is allowed by convert(), e.g.
            - m= : molality (mol/kg)
            - w= : mass fraction
            - x= : mole fraction
            - c= : molarity (mol/m^3)
            - r= : mass ratio (unitless)

        Output
        ------
        Value of property in SI units
        (float or array of floats depending on input)

        Attributes
        ----------
        .solutes --- list of available solutes
        .sources --- dict of available sources for every solute
        .default_sources --- default source for every solute
        .quantity --- type of physical quantity (e.g. 'surface tension')
        .unit --- unit of physical quantity (e.g. '[N/m]')
        """
        solute = self.default_solute if solute is None else solute
        source = self._get_source(source=source, solute=solute)
        formula = self.formulas[solute][source]

        if relative and not formula.with_water_reference:
            msg = f'relative=True not available for {formula.quantity} with {solute}'
            raise ValueError(msg)

        T = format_temperature(
            T,
            unit_in=unit,
            unit_out=formula.temperature_unit,
        )

        c = format_concentration(
            concentration=concentration,
            unit_out=formula.concentration_unit,
            solute=solute,
            converter=convert,
        )

        formula.check_validity_range('concentration', value=c)
        formula.check_validity_range('temperature', value=T)

        result = formula.calculate(c, T)

        if formula.with_water_reference:
            val_0, val = result
            if relative:
                return format_output_type(val / val_0)
            else:
                return format_output_type(val)

        return format_output_type(result)

    def _get_source(self, source=None, solute=None):
        """Return source if it's in sources, default_source if None."""
        solute = self.default_solute if solute is None else solute
        if source is None:
            return self.default_sources[solute]
        if source in self.sources[solute]:
            return source
        msg = f'Source can only be one of {self.sources} for {solute}'
        raise ValueError(msg)
