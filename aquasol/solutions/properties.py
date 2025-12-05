"""Main module to calculate the properties of aqueous solutions."""

# TODO: add densities expression of Clegg & Wexler 2011 (eq. 24)
# TODO: add expression of Pitzer 1982 (source of CRC Handbook)
# TODO: write more comprehensive examples


from .convert import convert

from ..properties import SolutionProperty, SolutionSolubilityProperty

from ..formulas.solutions.activity_coefficient import ActivityCoefficientFormulas
from ..formulas.solutions.water_activity import WaterActivityFormulas
from ..formulas.solutions.density import DensityFormulas
from ..formulas.solutions.surface_tension import SurfaceTensionFormulas
from ..formulas.solutions.electrical_conductivity import ElectricalConductivityFormulas
from ..formulas.solutions.refractive_index import RefractiveIndexFormulas
from ..formulas.solutions.viscosity import ViscosityFormulas
from ..formulas.solutions.solubility import SolubilityFormulas


class SolutionProperty_Full(SolutionProperty):
    """Solution property with full converter (including molarity).

    Is used to prevent circular import problems
    (because SolutionProperty is also used to define the density function used
    in convert())
    """
    # See SolutionProperty for explanation of necessity of staticmethod()
    converter = staticmethod(convert)


class ActivityCoefficient(SolutionProperty_Full):
    """Molal activity coefficient (Ɣ) of solute in a solution (a_s = Ɣ * m / mref)

    Examples
    --------
    - activity_coefficient(m=6.1)  # at saturation for NaCl
    - activity_coefficient(solute='KCl', T=50, m=[2, 4, 6])  # concentration as iterable
    """
    Formulas = ActivityCoefficientFormulas
    quantity = 'activity coefficient'
    unit = '[-]'


class WaterActivity(SolutionProperty_Full):
    """Water activity of a solution(aq) at given concentration and temperature

    Examples
    --------
    - water_activity(x=0.1) returns a_w for a mole fraction of 0.1 of NaCl
    - water_activity(w=0.2) returns a_w for a mass fraction of 0.2 of NaCl
    - water_activity(c=5000) returns a_w for a molality of 5 mol/L of NaCl
    - water_activity(m=6) returns a_w for a molality of 6 mol/kg of NaCl
    - water_activity('LiCl', m=6): same for LiCl
    - water_activity('LiCl', m=6, T=30): same for LiCl at 30°C
    - water_activity('LiCl', 293, 'K', m=6): same for LiCl at 293K.
    - water_activity(solute='CaCl2', T=50, m=[2, 4, 6])  # concentration as iterable
    """
    Formulas = WaterActivityFormulas
    quantity = 'water activity'
    unit = '[-]'


class Density(SolutionProperty_Full):
    """Density of a solution(aq) at a given concentration and temperature

    Examples
    --------
    - density(w=0.1) returns the density of a NaCl solution, calculated with
    Simion equation for a mass fraction of 0.1 at a temperature of 25°C.
    - density('LiCl', 300, 'K', m=6) density of a LiCl solution at 300K
    for a molality of 6 mol/kg.
    - density(source='Tang', x=0.1), density of NaCl solution at a mole
    fraction of 0.1, calculated with the equation from Tang.
    - density(c=5000, relative=True), relative density of NaCl solution at
    a concentration of 5 mol/L.
    """
    Formulas = DensityFormulas
    quantity = 'density'
    unit = '[kg/m^3]'


class SurfaceTension(SolutionProperty_Full):
    """Surface tension of a solution(aq) at a given concentration and temperature

    Examples
    --------
    - surface_tension(x=0.05) returns surface tension of an aqueous NaCl
    solution at 25°C and a mole fraction of 5%
    - surface_tension('LiCl', w=0.1) returns the surface tension of a LiCl
    solution at 25°C and weight fraction of 10%
    - surface_tension('CaCl2', 20, m=6) returns the surface tension of
    a CaCl2 solution at 20°C and molality 6 mol/kg
    - surface_tension('CaCl2', 300, 'K', c=5e3) returns the surface tension of
    a CaCl2 solution at 300K and molarity of 5 mol/L
    - surface_tension(x=[0.02, 0.04, 0.08])  # iterable concentration is ok
    """
    Formulas = SurfaceTensionFormulas
    quantity = 'surface tension'
    unit = '[N/m]'


class ElectricalConductivity(SolutionProperty_Full):
    """Electrical conductivity of an aqueous solution at a given concentration.

    Examples
    --------
    - electrical_conductivity(c=1000)  # 1 molar NaCl conductivity
    - electrical_conductivity(solute='KCl', m=0.1)
    - electrical_conductivity(solute='KCl, m=2.2, T=50)  # at 50°C

    (Note: arrays are accepted for concentration and temperature)
    """
    Formulas = ElectricalConductivityFormulas
    quantity = 'electrical conductivity'
    unit = '[S/m]'


class RefractiveIndex(SolutionProperty_Full):
    """Refractive index of a solution as a function of concentration and temperature

    Examples
    --------
    - refractive_index(x=0.1) returns n for a mole fraction of 0.1 of NaCl
    - refractive_index(w=0.2) returns n for a mass fraction of 0.2 of NaCl
    - refractive_index(c=5000) returns n for a molality of 5 mol/L of NaCl
    - refractive_index(m=3) returns n for a molality of 6 mol/kg of NaCl
    - refractive_index('KCl', m=3): same for KCl
    - refractive_index('KCl', m=3, T=30): same for KCl at 30°C
    - refractive_index('KCl', 293, 'K', m=3): same for KCl at 293K.
    """
    Formulas = RefractiveIndexFormulas
    quantity = 'refractive index'
    unit = '[-]'


class Viscosity(SolutionProperty_Full):
    """Viscosity of a solution as a function of concentration and temperature

    Examples
    --------
    - viscosity(x=0.1) returns η for a mole fraction of 0.1 of NaCl
    - viscosity(w=0.2) returns η for a mass fraction of 0.2 of NaCl
    - viscosity(c=5000) returns η for a molality of 5 mol/L of NaCl
    - viscosity(m=3) returns η for a molality of 6 mol/kg of NaCl
    - viscosity('KCl', m=3): same for KCl
    - viscosity('KCl', m=3, T=30): same for KCl at 30°C
    - viscosity('KCl', 293, 'K', m=3): same for KCl at 293K.
    """
    Formulas = ViscosityFormulas
    quantity = 'viscosity'
    unit = '[Pa.s]'


# ===== Solubility (a bit different because depends only on temperature) =====


class Solubility(SolutionSolubilityProperty):
    """Solubility as a function of temperature.

    Examples
    --------
    - solubility()                   # solubility (molality) of NaCl at 25°C
    - solubility(T=40)               # solubility (molality) of NaCl at 40°C
    - solubility(T=40, out='x')      # same, but in terms of mole fraction
    - solubility(T=40, out='c')      # same, but in terms of molarity (mol/m^3)
    - solubility('KCl', T=303.15, unit='K')  # solubility of KCl at 30°C
    - solubility(T=[0, 10, 20, 30])          # iterables accepted too
    - solubility('Na2SO4')           # solubility of Na2SO4 at 25°C
    """
    Formulas = SolubilityFormulas
    quantity = 'solubility'
    converter = staticmethod(convert)


# ================ GENERATE USABLE OBJECTS FROM ABOVE CLASSES ================

activity_coefficient = ActivityCoefficient()
water_activity = WaterActivity()
density = Density()
surface_tension = SurfaceTension()
electrical_conductivity = ElectricalConductivity()
refractive_index = RefractiveIndex()
viscosity = Viscosity()
solubility = Solubility()
