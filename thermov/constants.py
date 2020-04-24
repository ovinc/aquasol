"""Module with values of constants useful for solutions.

Note: dictionaries written in alphabetical order.

CONTENTS
--------
General properties:
    - Na (float): Avogadro's constant
    - R (float): molar gas constant
Water properties:
    - Mw (float): molar mass of water in kg / mol
    - Tc (float): critical temperature in K
    - Pc (float): critical pressure in MPa
Ion properties in dictionaries (keys : ion name, e.g. 'Cl')
    - weight_cations: molecular weight of cations in Daltons
    - weight_anions: molecular weight of anions in Daltons
Solute properties as dictionaries (keys: solute name, e.g. 'NaCl')
    - dissociation_numbers: tuple of  number of cations and anions released
    - charge_numbers: tuple of unit charges of cation and anion
Solute properties as functions:
    - molar_mass(solute). Input: solute name (e.g. 'NaCl'), output M in kg / mol

SOURCES
-------
CRC Handbook of Physics and Chemistry:
    - Thermodynamic Properties of Aqueous Ions
    http://hbcponline.com/faces/documents/05_04/05_04_0001.xhtml
    - Recommended values of the fundamental physical constants
    http://hbcponline.com/faces/documents/01_01/01_01_0001.xhtml
    - Fixed-point properties of H20 and D20
    http://hbcponline.com/faces/documents/06_04/06_04_0001.xhtml

IAPWS, Release on Surface Tension of Ordinary Water Substance
IAPWS, London, September 1994.

"""

# TODO: automatic detection of ion and cation from solute name (regex?),
# especially for the function molar_mass

# ============================= GENERAL CONSTANTS ============================

Na = 6.02214085774e23  # Avogadro's constant
R = 8.314459848  # molar gas constant in J/(mol.K)

# ============================== WATER PROPERTIES ============================

Mw = 18.015268e-3  # molar mass in kg / mol
Tc = 647.096  # critical temperature in K (IAPWS 2014)
Pc = 22.064e6  # critical pressure in Pa (CRC Handbook)

# =========================== SOLUTE/IONS PROPERTIES =========================

solute_list = ['CaCl2', 'KCl', 'LiCl', 'NaCl']

# Individual ion molecular weights in Daltons --------------------------------
weight_cations = {'Ca': 40.078,
                  'K': 39.098,
                  'Li': 6.94,
                  'Na': 22.99,
                  }
weight_anions = {'Br': 79.904,
                 'Cl': 35.453,
                 'SO3': 80.063,
                 'SO4': 96.063,
                 }

# Number of ions per solute molecule after dissociation, for cation and anion
dissociation_numbers = {'CaCl2': (1, 2),
                        'KCl': (1, 1),
                        'LiCl': (1, 1),
                        'NaCl': (1, 1),
                        }

# Unit charges of cation and anion in the solute -----------------------------
charge_numbers = {'CaCl2': (2, 1),
                  'KCl': (1, 1),
                  'LiCl': (1, 1),
                  'NaCl': (1, 1),
                  }

# Individual ions composing the molecule -------------------------------------
individual_ions = {'CaCl2': ('Ca', 'Cl'),
                   'KCl': ('K', 'Cl'),
                   'LiCl': ('Li', 'Cl'),
                   'NaCl': ('Na', 'Cl'),
                   }

# calculation of molar mass from the molecular weights -----------------------
def molar_mass(solute):
    """Return molar mass of solute compound in kg / mol."""
    try:
        cation, anion = individual_ions[solute]
    except KeyError:
        raise KeyError(f'{solute} molecular/molar mass data not available')

    m1, m2 = weight_cations[cation], weight_anions[anion]
    nu1, nu2 = dissociation_numbers[solute]
    mtot = nu1 * m1 + nu2 * m2

    return mtot * 1e-3







