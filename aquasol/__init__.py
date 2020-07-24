"""Thermodynamic relations for water and solutions"""

# TODO: write unittests
# TODO: Switch automatically to another equation if outside of range.

from . import solutions, water

# Shortcuts

from .water import vapor_pressure as ps
from .water import dewpoint as dp

from .solutions import water_activity as aw
from .solutions import aw_to_conc as ac
from .solutions import convert as cv

__version__ = 0.2
