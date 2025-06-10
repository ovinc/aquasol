"""
Gathers the formulas for the density of glycerol-water solutions.

Sources
-------

- Volk, A. & Kähler, C. J. 
Density model for aqueous glycerol solutions. 
Exp Fluids 59, 75 (2018). 
"""

from ...general import SolutionFormula

from .volk import density_water_glycerol, water_density


class Density_Glycerol_Volk(SolutionFormula):

    source = 'Volk'
    solute = 'glycerol'
    
    temperature_unit = 'C'
    temperature_range = (15, 30)

    concentration_unit = 'w'
    concentration_range = (0, 1)

    with_water_reference = True
    default = True

    def calculate(self, w, T):
        rho_w = water_density(T)
        return rho_w, density_water_glycerol(w, T)


Density_Glycerol_Formulas = (
    Density_Glycerol_Volk,
)