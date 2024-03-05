"""Literature references used with the aquasol module
"""

from dataclasses import dataclass


@dataclass
class Source:
    """Literature source."""
    name: str
    authors: str
    title: str
    journal: str
    pages: tuple
    year:int
    note: str = ''


source_wexler = Source(
    name='Wexler',
    authors='A. Wexler, L. Greenspan',
    title='Vapor Pressure Equation for Water in the Range 0 to 100°C',
    journal='Journal of Research of the National Bureau of Standards - A. Physics and Chemistry',
    year=1971,
    note='Psat expression, valid from 0 to 100°C. We use Equation (17) and not the simplified Equations 18a-c.'
)

source_bridgeman = Source(
    name='Bridgeman',
    authors='O. C. Bridgeman, E. W. Aldrich',
    title='Vapor Pressure Tables for Water',
    journal='Journal of Heat Transfer',
    year=1964,
    note='Psat expression, valid from 0 to 374.15°C.'
)

source_wagner = Source(
    name='Wagner',
    authors='W. Wagner, A. Pruß',
    title='The IAPWS Formulation 1995 for the Thermodynamic Properties of Ordinary Water Substance for General and Scientific Use',
    journal='Journal of Physical and Chemical Reference Data',
    year=2002,
    note='Psat expression from IAPWS; temperature validity range seems to be 0 - 1000°C. Equation is (2.5) page 398.'
)
