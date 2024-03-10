"""Properties of solutions."""

# TODO: add viscosity, diffusivity
# TODO: add saturation concentration of different solutes
# TODO: add partial molar volumes

from .properties import activity_coefficient, water_activity
from .properties import density, surface_tension
from .properties import refractive_index, electrical_conductivity
from .properties import solubility

from .convert import convert
from .invert import aw_to_conc
from .extend import osmotic_pressure, osmotic_coefficient, aw_saturated

from ..formulas.solutions.ionic import ion_quantities, ionic_strength
