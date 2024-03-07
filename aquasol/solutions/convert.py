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
from ..constants import molar_mass

from ..check import check_solute, check_units
from ..format import format_input_type, format_output_type

from .formulas.basic_conversions import basic_convert
from .formulas.basic_conversions import allowed_units as basic_units

from .general import calculation


# ================================== Config ==================================

add_units = ['c']
allowed_units = basic_units + add_units

# =========================== MAIN CONVERT FUNCTION ==========================


def convert(
    value,
    unit1,
    unit2,
    solute='NaCl',
    T=25,
    unit='C',
    density_source=None,
    density_wmin=0,
    density_wmax=0.99,
):
    """Convert between different concentration units for solutions.

    Parameters
    ----------
    - value (float): value to convert
    - unit1 (str): its unit.
    - unit2 (str): unit to convert to.
    - solute (str): name of solute (default 'NaCl').
    - T: temperature
    - unit: unit of temperature (should be 'C' or 'K'), only used for molarity

    Additional parameters are available when converting to/from molarity,
    because knowledge of solution density is required:
    - density_source: which formula to use to calculate density when converting
                      to/from molarity (None = default).
    - density_wmin: min mass fraction to consider when inverting molarity(w)
                    for iterative search (only when converting FROM molarity)
    - density_wmin: max mass fraction to consider when inverting molarity(w)
                    for iterative search (only when converting FROM molarity)

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
        w = molarity_to_w(
            c=value,
            solute=solute,
            T=T,
            unit=unit,
            source=density_source,
            wmin=density_wmin,
            wmax=density_wmax,
        )
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
            return w_to_molarity(
                w=w,
                solute=solute,
                T=T, unit=unit,
                source=density_source,
            )

        else:
            # This case should in principle never happen, except if bug in
            # logics of code above
            raise ValueError('Unknown error --  please check code of convert() function.')


# ============================== DENSITY FUNCTION ============================

def basic_density(solute, T=25, unit='C', source=None, **concentration):
    """Return the density of an aqueous solution at a given concentration.

    Simplified version of main density function, with only basic units
    to avoid circular imports of the density module when trying to use
    molarity as a unit.

    Uses the default formula for density as defined in the density submodules.

    Parameters
    ----------
    - solute (str): solute name, default 'NaCl'
    - T (float): temperature in K
    - source: literature source to calculate density (None = default)
    - **concentration: kwargs with any basic unit ('x', 'w', 'm', 'r')

    Output
    ------
    - density (kg/m^3)
    """
    parameters = T, unit, concentration
    _, rho = calculation(
        propty='density',
        solute=solute,
        source=source,
        parameters=parameters,
        converter=basic_convert,
    )
    return rho


# ============================= MOLARITY FUNCTIONS ===========================


def w_to_molarity(w, solute, T=25, unit='C', source=None):
    """Calculate molarity of solute from weight fraction at temperature T in °C"""
    check_solute(solute, solute_list)
    M = molar_mass(solute)
    rho = basic_density(solute=solute, T=T, unit=unit, source=source, w=w)
    return rho * w / M


def molarity_to_w(c, solute, T=25, unit='C', source=None, wmin=0, wmax=0.99):
    """Calculate weight fraction of solute from molarity at temperature T in °C.

    Note: can be slow because of inverting the function each time.
    """
    check_solute(solute, solute_list)

    def molarity(w):
        with warnings.catch_warnings():      # this is to avoid always warnings
            warnings.simplefilter('ignore')  # which pop up due to wmax being high
            return w_to_molarity(
                w=w,
                solute=solute,
                T=T,
                unit=unit,
                source=source,
            )

    weight_fraction = inversefunc(molarity, domain=[wmin, wmax])
    w = weight_fraction(c)

    # HACK: this is to give a warning if some parameters out of range when
    # applying the value found for w
    _ = basic_density(solute=solute, T=T, unit=unit, source=source, w=w)

    return format_output_type(w)
