"""
Gathers the formulas for the water activity of glycerol-water solutions.

Sources
-------

- Zhang, L., Grace, P. M. & Sun, D.-W. 
An accurate water activity model for glycerol solutions and its implementation on moisture sorption isotherm determination. 
Drying Technology 40, 2404–2413 (2022).
"""

from ...general import SolutionFormula

from .zhang import water_activity_glycerol


class WaterActivity_Glycerol_Zhang(SolutionFormula):

    source = 'Zhang'
    solute = 'glycerol'
    
    temperature_unit = 'K'
    temperature_range = (273.15, 373.15)

    concentration_unit = 'x'    
    concentration_range = (0, 97.5e-2)

    with_water_reference = False
    default = True

    def calculate(self, x, T):
        return water_activity_glycerol(x, T)
    

WaterActivityFormulas_Glycerol = (
    WaterActivity_Glycerol_Zhang,
)
