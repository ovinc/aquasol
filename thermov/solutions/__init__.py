"""Properties of solutions."""

# TODO: write unittests
# TODO: add viscosity, diffusivity
# TODO: add saturation concentration of different solutes
# TODO: add solute activity
# TODO: add partial molar volumes
# TODO: Switch automatically to another equation if outside of range.


from .properties import density, water_activity, surface_tension
from .convert import convert, ionic_strength, ion_quantities