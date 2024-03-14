"""Classes to describe specific formulas for water and solutions"""

from warnings import warn

import numpy as np


class Formula:
    """base class for formulas for water/solution properties"""

    # To be defined in subclasses
    source =''
    input_types = ()
    default = False  # Change to True to select default source

    def __repr__(self):
        msg = f'{self.source} formula'
        if self.default:
            msg += ' [default]'
        msg += '; '
        for input_type in self.input_types:
            validity_info = self._get_range_and_unit(input_type)
            v1, v2 = validity_info['range']
            unit = validity_info['unit']
            if v1 == v2:
                value = f'{v1}[{unit}]'
            else:
                value = f'{v1}-{v2}[{unit}]'
            msg += f"{input_type} {value} "
        return msg

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
                f'({unit} in [{val_min}-{val_max}]) for {self.source}.'
                f'[{self.solute}]',
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
    crystal = None   # because several crystal forms are possible
    crystal_hydration = None  # put integer if crystal is hydrated
    solute = None  # if not provided, extracted automatically from cystal name

    temperature_unit = None
    temperature_range = None

    # Do not change below ----------------------------------------------------

    input_types = 'temperature',

    def __init__(self):
        super().__init__()
        if self.solute is None:
            components = self.crystal.split(',')
            if len(components) > 2:
                raise ValueError(f'Crystal {self.crystal} not recognized')
            elif len(components) == 1:
                self.solute = self.crystal
            else:
                solute, _ = components
                self.__class__.solute = solute
