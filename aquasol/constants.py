"""Module with values of constants useful for solutions.

Note: dictionaries written in alphabetical order.

CONTENTS
--------
General properties:
    - Na (float): Avogadro's constant
    - R (float): molar gas constant
    - Patm (float): atmospheric pressure in Pa
Water properties:
    - Mw (float): molar mass of water in kg / mol
    - Tc (float): critical temperature in K
    - Pc (float): critical pressure in Pa
    - rhoc (float): critical density in kg / m^3
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
    - Physical Constants of Inorganic Compounds
    https://hbcp.chemnetbase.com/faces/documents/04_02/04_02_0001.xhtml
    - Thermodynamic Properties of Aqueous Ions
    http://hbcponline.com/faces/documents/05_04/05_04_0001.xhtml
    - Recommended values of the fundamental physical constants
    http://hbcponline.com/faces/documents/01_01/01_01_0001.xhtml
    - Fixed-point properties of H20 and D20
    http://hbcponline.com/faces/documents/06_04/06_04_0001.xhtml

IAPWS, Release on Surface Tension of Ordinary Water Substance
IAPWS, London, September 1994.

"""

# ============================= GENERAL CONSTANTS ============================

Na = 6.02214085774e23  # Avogadro's constant
R = 8.314459848  # molar gas constant in J/(mol.K)
Patm = 101325  # atmospheric pressure in Pa

# ============================== WATER PROPERTIES ============================

Mw = 18.015268e-3  # molar mass in kg / mol
Tc = 647.096  # critical temperature in K (IAPWS 2014)
Pc = 22.064e6  # critical pressure in Pa (CRC Handbook & IAPWS)
rhoc = 322    # critical density in kg/m^3 (CRC Handbook & IAPWS)

# =========================== SOLUTE/IONS PROPERTIES =========================

solute_list = [
    'AlCl3',
    'CaCl2',
    'K2SO4',
    'KCl',
    'KI',
    'KNO3',
    'LiCl',
    'MgCl2',
    'MgSO4',
    'Na2SO4',
    'NaCl',
    'NaNO3',
]

# Individual ion molecular weights in Daltons --------------------------------
weight_cations = {
    'Al': 26.982,
    'Ca': 40.078,
    'K': 39.098,
    'Li': 6.94,
    'Mg': 24.305,
    'Na': 22.99,
}

weight_anions = {
    'Br': 79.904,
    'Cl': 35.453,
    'I': 126.904,
    'NO3': 62.005,
    'SO3': 80.063,
    'SO4': 96.063,
}

# Number of ions per solute molecule after dissociation, for cation and anion
dissociation_numbers = {
    'AlCl3': (1, 3),
    'CaCl2': (1, 2),
    'K2SO4': (2, 1),
    'KCl': (1, 1),
    'KI': (1, 1),
    'KNO3': (1, 1),
    'LiCl': (1, 1),
    'MgCl2': (1, 2),
    'MgSO4': (1, 1),
    'Na2SO4': (2, 1),
    'NaCl': (1, 1),
    'NaNO3': (1, 1),
}

# Unit charges of cation and anion in the solute -----------------------------
charge_numbers = {
    'AlCl3': (3, 1),
    'CaCl2': (2, 1),
    'K2SO4': (1, 2),
    'KCl': (1, 1),
    'KI': (1, 1),
    'KNO3': (1, 1),
    'LiCl': (1, 1),
    'MgCl2': (2, 1),
    'MgSO4': (2, 2),
    'Na2SO4': (1, 2),
    'NaCl': (1, 1),
    'NaNO3': (1, 1),
}

# Individual ions composing the molecule -------------------------------------
individual_ions = {
    'AlCl3': ('Al', 'Cl'),
    'CaCl2': ('Ca', 'Cl'),
    'K2SO4': ('K', 'SO4'),
    'KCl': ('K', 'Cl'),
    'KI': ('K', 'I'),
    'KNO3': ('K', 'NO3'),
    'LiCl': ('Li', 'Cl'),
    'MgCl2': ('Mg', 'Cl'),
    'MgSO4': ('Mg', 'SO4'),
    'Na2SO4': ('Na', 'SO4'),
    'NaCl': ('Na', 'Cl'),
    'NaNO3': ('Na', 'NO3'),
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
