"""Refractive index of solutions according to Tan

Source
------
- Tan (default) : "Dependence of Refractive Index on Concentration and
Temperature in Electrolyte Solution, Polar Solution, Nonpolar Solution, and
Protein Solution", Tan & Huang, J. Chem. Eng. Data  (2015).
Valid from w = 0 to w = 0.25 and for temperatures between 20 and 45°C
"""

from ...general import SolutionFormula


class RefractiveIndex_Tan_Base(SolutionFormula):

    source ='Tan'

    temperature_unit = 'C'
    temperature_range = (20, 45)

    concentration_unit = 'w'

    with_water_reference = False

    def calculate(self, w, T):
        c = w * 100   # avoid using *= to not mutate objects in place
        n0, a1, a2, b1, b2 = self.coeffs.values()
        return n0 + a1 * c + a2 * c**2 + b1 * T + b2 * T**2


class RefractiveIndex_CaCl2_Tan_Base(RefractiveIndex_Tan_Base):
    solute = 'CaCl2'
    concentration_range = (0, 0.15)
    coeffs = {
        'n0': 1.3373,
        'a1': 2.5067e-3,
        'a2': -3.9e-8,
        'b1': -1.1122e-4,
        'b2': -4e-9,
    }


class RefractiveIndex_KCl_Tan_Base(RefractiveIndex_Tan_Base):
    solute = 'KCl'
    concentration_range = (0, 0.15)
    coeffs = {
        'n0': 1.3352,
        'a1': 1.6167e-3,
        'a2': -4e-7,
        'b1': -1.1356e-4,
        'b2': -5.7e-9,
    }


class RefractiveIndex_NaCl_Tan_Base(RefractiveIndex_Tan_Base):
    solute = 'NaCl'
    concentration_range = (0, 0.25)
    coeffs = {
        'n0': 1.3373,
        'a1': 1.7682e-3,
        'a2': 0,          # modified -5.8e-6 to 0 to fit the data adequately
        'b1': -1.3531e-4,
        'b2': -5.1e-8,
    }
