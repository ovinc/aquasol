"""Ionic strength and individual ionic concentrations etc.

SOURCES
-------
Personal calculations, and:
ionic strength expressed as molar fraction is used in Clegg et al. AST, 1997
ionic strength expressed as molality is more common, e.g. Pitzer 1973
"""

# Local imports
from ...format import format_input_type, check_solute
from ...constants import solute_list
from ...constants import dissociation_numbers, charge_numbers


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
        param, = concentration.keys()  # param is the chosen parameter ('x', 'm' or 'c')
        value, = concentration.values()  # corresponding value in the unit above
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
