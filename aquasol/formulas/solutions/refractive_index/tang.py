"""Refractive index of solutions according to Tang 1997

Source
------
Note:
    Tang 1997 cites other papers (e.g. Tang 1996) of his but compiles data
    in Table I. Some validity ranges (e.g. Na2SO4) are not correct in table I
    and I have taken them from the original sources.

Source
------
- Tang 1997 :
    Tang, I. N.
    Thermodynamic and optical properties of mixed-salt aerosols of atmospheric
    importance. Journal of Geophysical Research 102, 1883-1893 (1997).

Cites :

[NaCl]
Tang, I. N.
Chemical and size effects of hygroscopic aerosols on light scattering
coefficients.
Journal of Geophysical Research: Atmospheres 101, 19245-19250 (1996).

[Na2SO4]
Tang, I. N. & Munkelwitz, H. R.
Simultaneous Determination of Refractive Index and Density of an Evaporating
Aqueous Solution Droplet.
Aerosol Science and Technology 15, 201-207 (1991).

[Also Na2SO4]
Tang, I. N. & Munkelwitz, H. R.
Water activities, densities, and refractive indices of aqueous sulfates and
sodium nitrate droplets of atmospheric importance.
Journal of Geophysical Research 99, 18801 (1994).

[KCl]
Couldn't find the info in these other papers except Tang 1997
"""

from ....constants import Mw, molar_mass, SALTS
from ...general import SolutionFormula
from ..density.tang import Density_KCl_Tang_Base
from ..density.tang import Density_Na2SO4_Tang_Base
from ..density.tang import Density_NaCl_Tang_Base
from ..basic_conversions import basic_convert


IonicRefractions = {
    'Na': 0.86,
    'K': 3.21,
    'Cl': 8.09,
    'SO4': 13.44,
    'water': 3.717,
}


def ionic_refraction(solute):
    salt = SALTS[solute]
    R1 = IonicRefractions[salt.cation.molecule]
    R2 = IonicRefractions[salt.anion.molecule]
    nu1, nu2 = salt.stoichiometry
    return nu1 * R1 + nu2 * R2


density_classes = {
    'KCl': Density_KCl_Tang_Base,
    'Na2SO4': Density_Na2SO4_Tang_Base,
    'NaCl': Density_NaCl_Tang_Base,
}


class RefractiveIndex_Tang_Base(SolutionFormula):

    source = 'Tang'
    solute = None  # define in subclasses

    temperature_unit = 'C'
    temperature_range = (25, 25)

    concentration_unit = 'w'
    concentration_range = None  # define in subclasses

    with_water_reference = False

    def density(self, w, T):
        rho0, rho = density_classes[self.solute]().calculate(w=w, T=T)
        return rho

    def calculate(self, w, T):

        x = basic_convert(w, 'w', 'x', solute=self.solute)

        # ionic refraction
        Rw = IonicRefractions['water']
        Rs = ionic_refraction(self.solute)
        R = (1 - x) * Rw + x * Rs

        # molal volume
        rho = self.density(w=w, T=T)
        Ms = molar_mass(self.solute)
        V = ((1 - x) * Mw + x * Ms) / rho

        c = R / V * 1e-6  # factor 1e6 to go back to SI units

        return ((1 + 2 * c) / (1 - c)) ** (1 / 2)


# Note: I have adjusted the validity ranges below to the validity ranges
# of the density equation, because I did not see a stated validity range
# for the index of refraction


class RefractiveIndex_KCl_Tang_Base(RefractiveIndex_Tang_Base):
    solute = 'KCl'
    concentration_range = (0, 0.44)


class RefractiveIndex_Na2SO4_Tang_Base(RefractiveIndex_Tang_Base):
    solute = 'Na2SO4'
    concentration_range = (0, 0.68)


class RefractiveIndex_NaCl_Tang_Base(RefractiveIndex_Tang_Base):
    solute = 'NaCl'
    concentration_range = (0, 0.45)
