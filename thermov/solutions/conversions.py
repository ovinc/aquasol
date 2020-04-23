"""Global module for unit conversions for solutions.

Gathers conversions_basic and conversions_fancy in a user-friendly module."""

from ..constants import solute_list
from ..checks import check_solute, check_units

from .conversions_basic import convert as basic_convert
from .conversions_basic import allowed_units as basic_units
from .conversions_fancy import w_to_mass_ratio, mass_ratio_to_w
from .conversions_fancy import w_to_molarity, molarity_to_w


add_units = ['c', 'mass_ratio']
allowed_units = basic_units + add_units

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
    'x' (mole fraction), 'w' (weight fraction), 'm' (molality), 'mass_ratio'
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

    # No need to calculate anything if the in and out units are the same -----
    if unit1 == unit2:
        return value

    if set(units) == set(['w', 'mass_ratio']):
        # This is a special case where one does not need to know anything
        # about the solute to do the conversion
        if unit1 == 'w':
            return w_to_mass_ratio(value)
        else:
            return mass_ratio_to_w(value)
    else:
        check_solute(solute, solute_list)


    if unit1 in basic_units and unit2 in basic_units:
        return basic_convert(value, unit1, unit2, solute)

    # Check if it's unit1 which is a "fancy" unit and convert to w if so.
    if unit1 == 'c':
        w = molarity_to_w(value, solute, T, unit)
        value_in = w
        unit_in = 'w'
    elif unit1 == 'mass_ratio':
        w = mass_ratio_to_w(value)
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
        elif unit2 == 'mass_ratio':
            return w_to_mass_ratio(w)

        else:  # TODO: add the test of returning None in unit tests
            return None  # This case should never happen




