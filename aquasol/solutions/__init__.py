"""Properties of solutions."""

# TODO: add viscosity, diffusivity
# TODO: add saturation concentration of different solutes
# TODO: add partial molar volumes


# from .properties import activity_coefficient, water_activity
# from .properties import density, surface_tension
# from .properties import refractive_index, electrical_conductivity
# from .invert import aw_to_conc
# from .extend import osmotic_pressure, osmotic_coefficient
# from .formulas.water_activity import WaterActivity

from .properties import WaterActivity, Density

water_activity = WaterActivity()
density = Density()

from .convert import convert
from ..formulas.solutions.ionic import ion_quantities, ionic_strength
