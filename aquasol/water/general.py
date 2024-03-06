"""Global management of modules and formulas for water."""

from warnings import warn

import numpy as np

from ..format import format_temperature, format_output_type


class WaterFormula:
    """Generic class for formulas for water properties as a function of T"""

    # To be defined in subclasses
    source = ''
    temperature_unit = None
    temperature_range = None
    default = False  # Change to True to select default source

    # Do not change below
    input_types = 'temperature',

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


class WaterProperty:
    """Generic class for a property that can have various sources"""

    # Below, to define in subclasses
    Formulas = ()  # iterable of formulae available to calculate the property
    quantity = None
    unit = None

    def __init__(self):

        self.formulas = {}  # dict source_name: formula object

        for Formula in self.Formulas:

            formula = Formula()
            source = formula.name
            self.formulas[source] = formula

            if formula.default:
                self.default_source = source

        self.sources = tuple(self.formulas)  # only the source names

    def __repr__(self):
        return f'{self.quantity.capitalize()} {self.unit} (default: {self.default_source})'

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
