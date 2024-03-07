"""Parameter conversions for water and solutions. Only basic ones (w, x, m).

Basic parameters do not rely on volumetric and temperature dependent quantities
such as density.

One reason for this is to prevent circular imports
(e.g. more elaborate units such as molarity require knowledge about density,
and density uses basic conversions in its core)
Also, fancier things such as ionic strength are easier to treat separately

SOURCES
-------
CRC Handbook - Conversion Formulas for Concentration of Solutions
http://hbcponline.com/faces/documents/01_19/01_19_0001.xhtml
"""

# TODO -- write more comprehensive examples
# TODO -- add checks that inputs are within normal range (e.g. 0-1 for x or w)

from ...constants import molar_mass, Mw, solute_list
from ...format import check_solute, check_units

# Define what solutes and units are acceptable for conversion


allowed_units = ['x', 'w', 'm', 'r']


# ========================= MAIN CONVERSION FUNCTION =========================

def basic_convert(value, unit1, unit2, solute='NaCl'):
    """Convert between concentrations, molalities etc. for solutions.

    Parameters
    ----------
    - value (float): value to convert
    - unit1 (str): its unit.
    - unit2 (str): unit to convert to.
    - solute (str): name of solute, (default 'NaCl').

    solute has to be in the solute list in the constants module
    unit1 and unit2 have to be in the allowed units list :
    'x' (mole fraction.), 'w' (weight frac.), 'm' (molality), 'r' (mass ratio)

    Output
    ------
    Converted value (dimensionless or SI units)

    Examples
    --------
    - convert(0.4, 'w', 'x'): mass fraction of 0.4 into mole fraction for NaCl
    - convert(10, 'm', 'w'): molality of 10 mol/kg into mass fraction for NaCl
    - convert(10, 'm', 'w', 'LiCl'): same but for LiCl.
    """

    # No need to calculate anything if the in and out units are the same -----
    if unit1 == unit2:
        return value

    check_solute(solute, solute_list)
    check_units([unit1, unit2], allowed_units)

    # Get useful quantities related to solute --------------------------------
    M = molar_mass(solute)         # molar mass of solute, kg/mol

    if unit1 == 'w':  # weight fraction to other quantities ------------------

        w = value

        if unit2 == 'x':
            return (w / M) / (w / M + (1 - w) / Mw)

        elif unit2 == 'm':
            return w / ((1 - w) * M)

        elif unit2 == 'r':
            return w / (1 - w)

    if unit1 == 'x':  # mole fraction to other quantities --------------------

        x = value

        if unit2 == 'w':
            return x * M / (x * M + (1 - x) * Mw)

        elif unit2 == 'm':
            return 1 / Mw * x / (1 - x)

        elif unit2 == 'r':
            return M / Mw * x / (1 - x)

    if unit1 == 'm':   # molality to other quantities ------------------------

        m = value

        if unit2 == 'w':

            return m * M / (1 + m * M)

        elif unit2 == 'x':
            return m * Mw / (1 + Mw * m)

        elif unit2 == 'r':
            return M * m

    if unit1 == 'r':  # mass ratio to other quantities --------------

        z = value

        if unit2 == 'w':
            return z / (1 + z)

        elif unit2 == 'x':
            return z / M / (z / M + 1 / Mw)

        elif unit2 == 'm':
            return z / M
