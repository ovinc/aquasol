"""Module with values of constants useful for solutions.

Note: dictionaries written in alphabetical order.

CONTENTS
--------
Fundamental constants:
    - k (float): Boltzmann's constant
    - Na (float): Avogadro's constant
    - e (float): elementary charge
    - C (float): speed of light in vacuum
Other constants:
    - R (float): ideal gas constant
    - Patm (float): atmospheric pressure in Pa
    - epsilon0: electric permittivity in vacuum
    - mu0: magnetic permeability in vacuum
Water properties:
    - Mw (float): molar mass of water in kg / mol
    - Tc (float): critical temperature in K
    - Pc (float): critical pressure in Pa
    - rhoc (float): critical density in kg / m^3
Solute properties as functions:
    - get_salt(formula): return Salt object (see Salt docstring and help)
    - molar_mass(formula). Input: formula (e.g. 'NaCl'), output M in kg / mol

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
    - CODATA RECOMMENDED VALUES OF THE FUNDAMENTAL PHYSICAL CONSTANTS: 2018
    https://hbcp.chemnetbase.com/documents/18_01/18_01_0001.xhtml

IAPWS, Release on Surface Tension of Ordinary Water Substance
IAPWS, London, September 1994.

"""

# =========================== FUNDAMENTAL CONSTANTS ==========================

k = 1.380_649e-23   # Boltzmann's constant [J / K]
Na = 6.022_140_76e23    # Avogadro's constant [1/mol]
e = 1.602_176_634e-19   # elementary charge [C]
C = 299_792_458         # speed of light in vacuum [m/s]

# ============================= Other constants ==============================

R = k * Na
Patm = 101_325                   # atmospheric pressure [Pa]
epsilon0 = 8.854_187_8128e-12    # electric permittivity in vacuum
mu0 = 1.256_637_062_12e-6        # magnetic permeability in vacuum

# ============================== WATER PROPERTIES ============================

Mw = 18.015268e-3  # molar mass in kg / mol
Tc = 647.096  # critical temperature in K (IAPWS 2014)
Pc = 22.064e6  # critical pressure in Pa (CRC Handbook & IAPWS)
rhoc = 322    # critical density in kg/m^3 (CRC Handbook & IAPWS)

# =========================== SOLUTE/IONS PROPERTIES =========================


# Individual ions ------------------------------------------------------------


class Ion:
    """Representation of anions and cations"""

    def __init__(self, molecule, name, charge, molecular_weight):
        self.molecule = molecule  # e.g. 'Cl'
        self.name = name          # e.g. 'chloride'
        self.charge = charge      # e.g. -1
        self.molecular_weight = molecular_weight  # in Daltons

    @property
    def ion_type(self):
        return 'cation' if self.charge > 0 else 'anion'

    def __repr__(self):
        charge_str = ''
        if abs(self.charge) > 1:
            charge_str += f'{abs(self.charge)}'
        charge_str += ('+' if self.charge > 0 else '-')
        return f'{self.name.capitalize()} {self.ion_type} {self.molecule}[{charge_str}]'


cations = (
    Ion('Al', name='aluminium', charge=3, molecular_weight=26.982),
    Ion('Ca', name='calcium', charge=2, molecular_weight=40.078),
    Ion('K', name='potassium', charge=1, molecular_weight=39.098),
    Ion('Li', name='lithium', charge=1, molecular_weight=6.94),
    Ion('Mg', name='magnesium', charge=2, molecular_weight=24.305),
    Ion('Na', name='sodium', charge=1, molecular_weight=22.99),
)

anions = (
    Ion('Br', name='bromide', charge=-1, molecular_weight=79.904),
    Ion('Cl', name='chloride', charge=-1, molecular_weight=35.453),
    Ion('I', name='iodide', charge=-1, molecular_weight=126.904),
    Ion('NO3', name='nitrate', charge=-1, molecular_weight=62.005),
    Ion('SO3', name='sulfite', charge=-2, molecular_weight=80.063),
    Ion('SO4', name='sulfate', charge=-2, molecular_weight=96.063),
)

CATIONS = {cation.name: cation for cation in cations}
ANIONS = {anion.name: anion for anion in anions}


#  Solutes / salts -----------------------------------------------------------

class Solute():
    """Base class for solutes, including salts"""

    def __init__(self, formula, molar_mass):

        self.formula = formula
        self.molar_mass = molar_mass


class Salt(Solute):
    """Representation of salt solute and its characteristics"""

    def __init__(self, cation, anion):
        """Name is e.g. 'NaCl'"""
        self.cation = CATIONS[cation]
        self.anion = ANIONS[anion]
        self.ions = self.cation, self.anion
        self.charges = tuple((ion.charge for ion in self.ions))
        self.stoichiometry = tuple(abs(ion.charge) for ion in reversed(self.ions))
        self.molecular_weight = self._get_weight()      # in Daltons

        super().__init__(
            formula=self._get_formula(), 
            molar_mass=self.molecular_weight * 1e-3,    # in kg/mol
        )

    def _get_formula(self):
        formula = ''
        for ion, coeff in zip(self.ions, self.stoichiometry):
            formula += ion.molecule
            if coeff > 1:
                formula += str(coeff)
        return formula

    def _get_weight(self):
        """In Daltons"""
        ion_coeffs = zip(self.ions, self.stoichiometry)
        ws = [ion.molecular_weight * coeff for ion, coeff in ion_coeffs]
        return sum(ws)

    def __repr__(self):
        return f'{self.cation.name.capitalize()} {self.anion.name} {self.formula}'


salts = (
    Salt('aluminium', 'chloride'),
    Salt('calcium', 'chloride'),
    Salt('potassium', 'sulfate'),
    Salt('potassium', 'chloride'),
    Salt('potassium', 'iodide'),
    Salt('potassium', 'nitrate'),
    Salt('lithium', 'bromide'),
    Salt('lithium', 'chloride'),
    Salt('magnesium', 'chloride'),
    Salt('magnesium', 'sulfate'),
    Salt('sodium', 'sulfate'),
    Salt('sodium', 'chloride'),
    Salt('sodium', 'nitrate'),
)

SALTS = {salt.formula: salt for salt in salts}


class NeutralSolute(Solute):
    """Representation of neutral solute and its characteristics"""

    def __repr__(self) -> str:
        return f'Neutral solute: {self.formula.capitalize()}'

neutral_solutes = (
    NeutralSolute(formula='glycerol', molar_mass=92.0938e-3),
)

NEUTRAL_SOLUTES = {solute.formula: solute for solute in neutral_solutes}


# Useful constants and functions ---------------------------------------------


SOLUTES = {**SALTS, **NEUTRAL_SOLUTES}  # more solutes (possibly non-salts) can be added later


def get_solute(formula):
    """Get salt object from its formula"""
    try:
        return SOLUTES[formula]
    except KeyError:
        raise ValueError(f'{formula} not in available solutes: {list(SOLUTES)}')


def molar_mass(formula):
    """Return molar mass of solute compound in kg / mol."""
    solute = get_solute(formula=formula)
    return solute.molar_mass
