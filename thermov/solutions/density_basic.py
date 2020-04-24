"""Simplified version of density of aqueous solutions, with only basic units
to avoid circular imports of the density module when trying to use molarity
as a unit.

Uses the default formula for density as defined in the density submodules.
"""

from .general import solution_calculation
from .conversions_basic import basic_convert as converter

def density_basic(solute, T=25, unit='C', **concentration):
    """Return the density of an aqueous solution at a given concentration.

    Parameters
    ----------
    - solute (str): solute name, default 'NaCl'
    - T (float): temperature in K
    - **concentration: kwargs with any basic unit ('x', 'w', 'm', 'mass_ratio')

    Output
    ------
    - density (kg/m^3)

    Sources
    -------
    Default source defined in each solute submodule.
    """

    # Dictionary of modules to load for every solute -------------------------
    modules = {'NaCl': 'density_formulas.nacl'}

    # set source to None to get default formula for density
    source = None

    # Calculate density using general solution calculation scheme -----------
    parameters = T, unit, concentration
    rho0, rho = solution_calculation(solute, source, modules, parameters, converter)

    return rho
