"""Thermodynamic & physico-chemical properties for water and aqueous solutions

Copyright Olivier Vincent (2020-2024)
(ovinc.py@gmail.com)

This software is a computer program whose purpose is to provide the
properties of water and aqueous solutions as a function of temperature
and/or concentration (along with other useful tools).

This software is governed by the CeCILL license under French law and
abiding by the rules of distribution of free software. You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author, the holder of the
economic rights, and the successive licensors have only limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading, using, modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean that it is complicated to manipulate, and that also
therefore means that it is reserved for developers and experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and, more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.
"""

# TODO: Switch automatically to another equation if outside of range?


# Shortcuts ------------------------------------------------------------------

from .water import vapor_pressure as ps
from .water import dewpoint as dp
from .water import kelvin_pressure as kp
from .water import kelvin_humidity as kh
from .water import kelvin_radius as kr
from .water import molar_volume as vm

from .solutions import water_activity as aw
from .solutions import aw_to_conc as ac
from .solutions import convert as cv

# ----------------------------------------------------------------------------

from importlib_metadata import version

__author__ = 'Olivier Vincent'
__version__ = version('aquasol')
__license__ = 'CeCILL-2.1'
