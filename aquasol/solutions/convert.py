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
import numpy as np

# Local imports
from ..constants import solute_list
from ..constants import molar_mass
from ..format import check_solute, check_units
from ..format import format_input_type, format_output_type, format_concentration
from ..properties import SolutionProperty

from ..formulas.solutions.basic_conversions import basic_convert
from ..formulas.solutions.basic_conversions import allowed_units as basic_units

from ..formulas.solutions.density import DensityFormulas


# ================================== Config ==================================


add_units = ['c']
allowed_units = basic_units + add_units


# ============== Reduced density class (avoid circular imports) ==============


class Density_Basic(SolutionProperty):
    """Density property with partial converter (without molarity).

    Is used to prevent circular import problems
    (because SolutionProperty is also used to define the density function used
    in convert())
    """
    # See SolutionProperty for explantion of staticmethod()
    converter = staticmethod(basic_convert)
    Formulas = DensityFormulas
    quantity = 'density'
    unit = ['kg/m^3']


density_basic = Density_Basic()


# ============================= MOLARITY FUNCTIONS ===========================


def w_to_molarity(w, solute, T=25, unit='C', source=None):
    """Calculate molarity of solute from weight fraction at temperature T in °C"""
    check_solute(solute, solute_list)
    M = molar_mass(solute)
    rho = density_basic(solute=solute, T=T, unit=unit, source=source, w=w)
    return rho * w / M


def _get_max_w(solute, T=25, unit='C', source=None, wmin=0, wmax=0.999):
    """Detect if density has a maximum, in which case the inversion fails."""
    ww = np.linspace(wmin, wmax, num=200)
    with warnings.catch_warnings():      # this is to avoid always warnings
        warnings.simplefilter('ignore')  # which pop up due to wmax being high
        rho = density_basic(solute=solute, T=T, unit=unit, source=source, w=ww)
    imax = np.argmax(rho)
    return ww[imax] # will be equal to wmax if function only increases


def molarity_to_w(c, solute, T=25, unit='C', source=None, wmin=0, wmax=0.999):
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

    # replace wmax if density goes through a maximum
    # (in order to prevent function inversion to fail)
    wmax = _get_max_w(
        solute=solute,
        T=T,
        unit=unit,
        source=source,
        wmin=wmin,
        wmax=wmax,
    )

    # Also prevents inversion fail, and provides more explicit error msg -----
    cmax = molarity(wmax)
    # Line below should always work because c is usually converted to np array
    # if it is a list or tuple etc.
    test = (c > cmax)

    try:  # won't work for an array
        cmax_exceeded = bool(test)
    except ValueError:
        cc = np.array(c).flatten()
        cmax_exceeded = any(cc > cmax)

    if cmax_exceeded:
        src = density_basic.get_source(solute=solute, source=source)
        msg = (
            f"Requested molality (c={c}) exceeds maximum available with "
            f"{src}'s density formula (cmax={round(cmax):_}), "
            f"corresponding to wmax={wmax:.3f}"
        )
        raise ValueError(msg)
    # ------------------------------------------------------------------------

    weight_fraction = inversefunc(molarity, domain=[wmin, wmax])
    w = weight_fraction(c)

    # This is to give a warning if some value(s) of w out of range when
    formula = density_basic.get_formula(solute=solute, source=source)
    c = format_concentration(
            concentration={'w': w},
            unit_out=formula.concentration_unit,
            solute=solute,
            converter=density_basic.converter,
        )
    formula.check_validity_range('concentration', value=c)

    return format_output_type(w)


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
    density_wmax=0.999,
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
        return basic_convert(
            value=value,
            unit1=unit1,
            unit2=unit2,
            solute=solute,
        )

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
        return basic_convert(
            value=value_in,
            unit1=unit_in,
            unit2=unit2,
            solute=solute,
        )

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
