"""Convert to/from various parameters (molarity, molality, x, w, etc.)

SOURCES
-------
Personal calculations, and:
ionic strength expressed as molar fraction is used in Clegg et al. AST, 1997
ionic strength expressed as molality is more common, e.g. Pitzer 1973
"""

# Standard Library
import warnings

# Non-standard imports
from pynverse import inversefunc

# Local imports
from ..constants import solute_list
from ..constants import molar_mass, dissociation_numbers, charge_numbers

from ..check import check_solute, check_units
from ..format import format_input_type, format_output_type

from .formulas.basic_conversions import basic_convert
from .formulas.basic_conversions import allowed_units as basic_units

from .general import calculation


# ================================== Config ==================================

add_units = ['c']
allowed_units = basic_units + add_units

# =========================== MAIN CONVERT FUNCTION ==========================


def convert(value, unit1, unit2, solute='NaCl', T=25, unit='C'):
    """Convert between different concentration units for solutions.

    Parameters
    ----------
    - value (float): value to convert
    - unit1 (str): its unit.
    - unit2 (str): unit to convert to.
    - solute (str): name of solute (default 'NaCl').
    - T: temperature
    - unit: unit of temperature (should be 'C' or 'K'), only used for molarity

    solute has to be in the solute list in the constants module and in the
    solutes with density data if unit1 or unit2 is molarity ('c').

    unit1 and unit2 have to be in the allowed units list :
    'x' (mole fraction), 'w' (weight fraction), 'm' (molality), 'r'
    (ratio of mass of solute to mass of solvent), 'c' (molarity in mol/m^3)

    Output
    ------
    Converted value (dimensionless or SI units)

    Examples
    --------
    - convert(0.4, 'w', 'x'): mass fraction of 0.4 into mole fraction for NaCl
    - convert(10, 'm', 'w'): molality of 10 mol/kg into mass fraction for NaCl
    - convert(10, 'm', 'w', 'LiCl'): same but for LiCl.
    - convert(5000, 'c', 'x'): molarity of 5 mol/m^3 to mole fraction for NaCl
    (assuming a temperature of T=25°C)
    - convert(5000, 'c', 'x', T=30): same but at 30°C.
    - convert(5000, 'c', 'x', T=293, unit='K'): same but at 293K
    - convert(5000, 'c', 'x', solute='LiCl'): for LiCl at 25°C
    """

    units = [unit1, unit2]
    check_units(units, allowed_units)

    value = format_input_type(value)  # allows for lists and tuples as inputs

    # No need to calculate anything if the in and out units are the same -----
    if unit1 == unit2:
        return value

    check_solute(solute, solute_list)

    if unit1 in basic_units and unit2 in basic_units:
        return basic_convert(value, unit1, unit2, solute)

    # Check if it's unit1 which is a "fancy" unit and convert to w if so.
    if unit1 == 'c':
        w = molarity_to_w(value, solute, T, unit)
        value_in = w
        unit_in = 'w'
    else:
        value_in = value
        unit_in = unit1

    if unit2 in basic_units:   # If unit2 is basic, the job is now easy
        return basic_convert(value_in, unit_in, unit2, solute)

    else:  # If not, first convert to w, then again to the asked unit

        w = basic_convert(value_in, unit_in, 'w', solute)
        if unit2 == 'c':
            return w_to_molarity(w, solute, T, unit)

        else:  # TODO: add the test of returning None in unit tests
            return None  # This case should never happen


# ============================== DENSITY FUNCTION ============================

def basic_density(solute, T=25, unit='C', **concentration):
    """Return the density of an aqueous solution at a given concentration.

    Simplified version of main density function, with only basic units
    to avoid circular imports of the density module when trying to use
    molarity as a unit.

    Uses the default formula for density as defined in the density submodules.

    Parameters
    ----------
    - solute (str): solute name, default 'NaCl'
    - T (float): temperature in K
    - **concentration: kwargs with any basic unit ('x', 'w', 'm', 'r')

    Output
    ------
    - density (kg/m^3)

    Sources
    -------
    Default source defined in each solute submodule.
    """
    source = None  # set source to None to get default formula for density
    parameters = T, unit, concentration
    rho0, rho = calculation('density', solute, source, parameters, basic_convert)

    return rho


# ============================= MOLARITY FUNCTIONS ===========================


def w_to_molarity(w, solute, T=25, unit='C'):
    """Calculate molarity of solute from weight fraction at temperature T in °C"""
    check_solute(solute, solute_list)
    M = molar_mass(solute)
    rho = basic_density(solute=solute, T=T, unit=unit, w=w)
    return rho * w / M


def molarity_to_w(c, solute, T=25, unit='C'):
    """Calculate weight fraction of solute from molarity at temperature T in °C.

    Note: can be slow because of inverting the function each time.
    """

    check_solute(solute, solute_list)

    wmax = 0.99  # max weight fraction allowed (for easy inverting of function)

    def molarity(w):
        with warnings.catch_warnings():      # this is to avoid always warnings
            warnings.simplefilter('ignore')  # which pop up due to wmax being high
            return w_to_molarity(w, solute, T, unit)

    weight_fraction = inversefunc(molarity, domain=[0, wmax])
    w = weight_fraction(c)

    # HACK: this is to give a warning if some parameters out of range when
    # applying the value found for w
    _ = basic_density(solute=solute, T=T, unit=unit, w=w)

    return format_output_type(w)


# ========================== INDIVIDUAL ION QUANTITIES =======================

def ion_quantities(solute, **concentration):
    """Return quantities x, m, c but defined for each ion instead of considering
    the solute as a single species. Used in ionic strength calculations.

    ion_quantities('NaCl', x=0.1) returns (x1, x2) where x1 is the mole fraction
    of Na+, x2 is that of Cl-.

    In this situation, one considers that there are three components in solution
    i.e. the cation (x1), the anion (x2) and the solvent (xw), with
    xi = ni / (ni + nj + nw).

    For molalities or concentrations, things are easier because these quantities
    are just multiplied by the dissociation number when considering individual
    ions compared to the solute as a whole. They are calculated using e.g.
    ion_quantities('NaCl', m=5.3) or ion_quantities('NaCl', c=4.8)
    """
    if len(concentration) == 1:
        [param] = concentration.keys()  # param is the chosen parameter ('x', 'm' or 'c')
        [value] = concentration.values()  # corresponding value in the unit above
    else:
        raise ValueError('kwargs must have exactly one keyword argument for solute concentration.')

    value = format_input_type(value)  # allows for lists and tuples as inputs

    check_solute(solute, solute_list)
    n1, n2 = dissociation_numbers[solute]

    if param == 'x':
        x = value
        ntot = n1 + n2
        x_interm = x / (1 + x * (ntot - 1))  # just for calculation
        x1 = n1 * x_interm
        x2 = n2 * x_interm
        return x1, x2

    elif param in ['m', 'c']:  # in this case, things are simply additive
        return n1 * value, n2 * value

    else:
        raise ValueError(f"quantity {param} not allowed, should be 'x', 'm' or 'c'.")


# =============================== IONIC STRENGTH =============================

def ionic_strength(solute, **concentration):
    """Ionic strength in terms of mole fraction (x), molality (m) or molarity (c)

    ionic_strength('NaCl', x=0.1) returns the mole fraction ionic strength (Ix)
    ionic_strength('NaCl', m=1.2) returns the molal ionic strength
    ionic_strength('NaCl', c=5.3) returns the molar ionic strength

    Note: output units is different for each case (same as input parameter, e.g.
    mol / m^3 for 'c').
    """
    check_solute(solute, solute_list)
    z1, z2 = charge_numbers[solute]
    y1, y2 = ion_quantities(solute, **concentration)
    I_strength = 0.5 * (y1 * z1 ** 2 + y2 * z2 ** 2)
    return I_strength

