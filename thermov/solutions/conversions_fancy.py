"""Upgrade basic conversions with more advanced parameters such as
molarity, mass ratio, ionic strength and individual ion quantities (xi, wi, mi etc.)

SOURCES
-------
Personal calculations, and:
ionic strength expressed as molar fraction is used in Clegg et al. AST, 1997
ionic strength expressed as molality is more common, e.g. Pitzer 1973
"""

# TODO -- add conversions from C to others (needs work on inverting w*rho(w))
# TODO -- write unittests or pytests
# TODO -- write more comprehensive examples
# TODO -- verify that everything is in SI units

import warnings
from pynverse import inversefunc

from ..constants import molar_mass, dissociation_numbers, charge_numbers, solute_list
from ..checks import check_solute
from .density import density

# =========================== MASS RATIO FUNCTIONS =============================

def w_to_mass_ratio(w):
    """Return ratio of solute mass to solvent mass from mass fraction w."""
    return w / (1 - w)


def mass_ratio_to_w(z):
    """Return mass fraction w from ratio of solute mass to solvent mass."""
    return z / (1 + z)


# ============================= MOLARITY FUNCTIONS =============================

def w_to_molarity(w, solute, T=25, unit='C'):
    """Calculate molarity of solute from weight fraction at temperature T in °C"""
    check_solute(solute, solute_list)
    M = molar_mass(solute)
    rho = density(solute=solute, T=T, unit=unit, w=w)
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
    _ = density(solute=solute, T=T, unit=unit, w=w)

    if len(w.shape) == 0:  # this is to return a scalar if a scalar is used as input
        return w.item()
    else:
        return w


# ========================== INDIVIDUAL ION QUANTITIES =========================

def ion_quantities(solute, **kwargs):
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
    if len(kwargs) == 1:
        [param] = kwargs.keys()  # param is the chosen parameter ('x', 'm' or 'c')
        [value] = kwargs.values()  # corresponding value in the unit above
    else:
        raise ValueError('kwargs must have exactly one keyword argument for solute concentration.')

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


# =============================== IONIC STRENGTH ===============================

def ionic_strength(solute, **kwargs):
    """Ionic strength in terms of mole fraction (x), molality (m) or molarity (c)

    ionic_strength('NaCl', x=0.1) returns the mole fraction ionic strength (Ix)
    ionic_strength('NaCl', m=1.2) returns the molal ionic strength
    ionic_strength('NaCl', c=5.3) returns the molar ionic strength

    Note: output units is different for each case (same as input parameter, e.g.
    mol / m^3 for 'c').
    """
    check_solute(solute, solute_list)
    z1, z2 = charge_numbers[solute]
    y1, y2 = ion_quantities(solute, **kwargs)
    I_strength = 0.5 * (y1 * z1 ** 2 + y2 * z2 ** 2)
    return I_strength

