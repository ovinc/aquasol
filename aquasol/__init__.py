"""Thermodynamic relations for water and solutions"""

# TODO: write Tests for solutions
# TODO: Switch automatically to another equation if outside of range.

from . import solutions, water

# Shortcuts

from .water import vapor_pressure as ps
from .water import dewpoint as dp
from .water import kelvin_pressure as kp
from .water import kelvin_humidity as kh
from .water import kelvin_radius as kr
from .water import molar_volume as vm

from .solutions import water_activity as aw
from .solutions import aw_to_conc as ac
from .solutions import convert as cv

from importlib_metadata import version

__author__ = 'Olivier Vincent'
__version__ = version('aquasol')
__license__ = 'BSD 3-Clause'
