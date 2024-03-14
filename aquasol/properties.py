"""Classes to describe properties containing one or multiple  formulas."""


from .format import format_temperature, format_concentration
from .format import format_output_type

# NOTE: convert() cannot be imported here due to circular import problems


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
            source = formula.source
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
        (see self.sources and self.default_source for more info)

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
        formula = self.get_formula(source=source)

        T = format_temperature(
            T,
            unit_in=unit,
            unit_out=formula.temperature_unit,
        )

        formula.check_validity_range('temperature', value=T)
        result = formula.calculate(T)
        return format_output_type(result)

    def get_source(self, source=None):
        """Return source if it's in sources, default_source if None."""
        if source is None:
            return self.default_source
        if source in self.sources:
            return source
        raise ValueError(f'Source can only be one of {self.sources}')

    def get_formula(self, source=None):
        """Return formula corresponding to source."""
        source = self.get_source(source=source)
        return self.formulas[source]


class SolutionProperty_Base(Property):
    """Generic class for a property of solutions (saturated or not)"""

    # Define in subclasses (is used to avoid importing convert() in this
    # module, because SolutionProperty is used to defined both the general
    # density and the reduced density used in convert())
    # CAUTION: when putting the converter function as attribute, put the
    # function in staticmethod(), because if not, it will be interpreted as a
    # bound method (and self will be passed as first argument)
    # See e.g. here: https://stackoverflow.com/questions/35321744/python-function-as-class-attribute-becomes-a-bound-method
    converter = None

    def _set_formulas(self, component_type='solute'):
        """Component type is 'solute' or 'crystal' (for saturated solutions)"""

        components = self._get_available_components(component_type)
        setattr(self, f'{component_type}s', components)

        self.formulas = {component: {} for component in components}
        self.sources = {}
        self.default_sources = {}

        for Formula in self.Formulas:

            formula = Formula()
            source = formula.source
            component = getattr(formula, component_type)

            self.formulas[component][source] = formula

            if formula.default:
                self.default_sources[component] = source

            # only the source names
            self.sources[component] = tuple(self.formulas[component])

    def _get_available_components(self, component_type='solute'):
        """Component type is 'solute', or 'crystal' (for saturated solutions)"""
        components = set()
        for Formula in self.Formulas:
            component = getattr(Formula, component_type)
            components.add(component)
        return tuple(components)


class SolutionProperty(SolutionProperty_Base):
    """Generic class for a property of solutions as a function of T/c"""

    # Change in subclasses if needed (e.g. if NaCl not available)
    default_solute = 'NaCl'

    def __init__(self):
        self._set_formulas(component_type='solute')

    def __repr__(self):
        return f'{self.quantity.capitalize()} {self.unit} (solutes: {self.solutes})'

    def get_solute(self, solute=None):
        return self.default_solute if solute is None else solute

    def get_source(self, solute=None, source=None):
        """Return source if it's in sources, default_source if None."""
        solute =self.get_solute(solute=solute)
        if source is None:
            return self.default_sources[solute]
        if source in self.sources[solute]:
            return source
        msg = f'Source can only be one of {self.sources} for {solute}'
        raise ValueError(msg)

    def get_formula(self, solute=None, source=None):
        """Return formula corresponding to source and solute (default if None)"""
        solute = self.get_solute(solute=solute)
        source = self.get_source(source=source, solute=solute)
        return self.formulas[solute][source]

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
        See self.sources and self.default_sources for more info

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
        solute = self.get_solute(solute=solute)
        formula = self.get_formula(source=source, solute=solute)

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
            converter=self.converter,
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


class SolutionSolubilityProperty(SolutionProperty_Base):
    """Class for describing solubility"""

    # Change in subclasses if needed (e.g. if NaCl not available)
    default_crystal = 'NaCl'

    def __init__(self):
        self._set_formulas(component_type='crystal')

    def __repr__(self):
        return f'{self.quantity.capitalize()} (crystals: {self.crystals})'

    def get_crystal(self, crystal=None):
        return self.default_crystal if crystal is None else crystal

    def get_source(self, crystal=None, source=None):
        """Return source if it's in sources, default_source if None."""
        crystal =self.get_crystal(crystal=crystal)
        if source is None:
            return self.default_sources[crystal]
        if source in self.sources[crystal]:
            return source
        msg = f'Source can only be one of {self.sources} for {crystal}'
        raise ValueError(msg)

    def get_formula(self, crystal=None, source=None):
        """Return formula corresponding to source and crystal (default if None)"""
        crystal = self.get_crystal(crystal=crystal)
        source = self.get_source(source=source, crystal=crystal)
        return self.formulas[crystal][source]

    def __call__(
        self,
        crystal=None,
        T=25,
        unit='C',
        source=None,
        out='m',
    ):
        """Calculate solution property as a function of temperature and composition

        Parameters
        ----------
        - crystal (str): crystal name (usually same as solute except if several
                                       crystalline forms)
        - T (float): temperature (default 25)
        - unit (str, default 'C'): 'C' for Celsius, 'K' for Kelvin
        - source (str, default None) : Source for the used equation, if None then
        gets the default source for the particular solute (defined in submodules).
        See self.sources and self.default_sources for more info
        - out: any unit that is allowed by convert(), e.g.
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
        """
        crystal = self.get_crystal(crystal=crystal)
        formula = self.get_formula(source=source, crystal=crystal)

        T = format_temperature(
            T,
            unit_in=unit,
            unit_out=formula.temperature_unit,
        )

        formula.check_validity_range('temperature', value=T)

        c_unit = formula.concentration_unit
        c_raw = formula.calculate(T)

        c = format_concentration(
            concentration={c_unit: c_raw},
            unit_out=out,
            solute=formula.solute,
            converter=self.converter,
        )

        return format_output_type(c)
