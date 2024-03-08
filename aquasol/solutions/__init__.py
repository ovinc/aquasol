"""Properties of solutions."""

# TODO: add viscosity, diffusivity
# TODO: add saturation concentration of different solutes
# TODO: add partial molar volumes

# from .properties import activity_coefficient, water_activity
# from .properties import density, surface_tension
# from .properties import refractive_index, electrical_conductivity
from .invert import aw_to_conc
from .extend import osmotic_pressure, osmotic_coefficient

from ..formulas.solutions.ionic import ion_quantities, ionic_strength
from .convert import convert
from .properties import water_activity, density, surface_tension

