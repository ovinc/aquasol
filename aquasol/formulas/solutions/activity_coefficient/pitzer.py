"""Activity of solutions according to Pitzer original paper.

NOTE: Almost identical in structure to water_activity.pitzer

Sources
-------
Pitzer, K. S. & Mayorga, G.
Thermodynamics of electrolytes. II.
Activity and osmotic coefficients for strong electrolytes with one or both
ions univalent.
J. Phys. Chem. 77, 2300-2308
(1973)
"""

from ...general import SolutionFormula
from ..pitzer import PitzerActivityOriginal


class ActivityCoefficient_Pitzer_Base(SolutionFormula):

    source = 'Pitzer'

    temperature_unit = 'K'
    temperature_range = (298.15, 298.15)

    concentration_unit = 'm'

    with_water_reference = False

    def calculate(self, m, T):
        pitz = PitzerActivityOriginal(T=T, solute=self.solute, **self.coeffs)
        return pitz.activity_coefficient(m=m)


# ============================ Different solutes =============================


class ActivityCoefficient_NaCl_Pitzer_Base(ActivityCoefficient_Pitzer_Base):
    solute = 'NaCl'
    concentration_range = (0, 6)
    coeffs = {
        'beta0': 0.0765,
        'beta1': 0.2664,
        'C_phi': 0.00127,
    }


class ActivityCoefficient_LiCl_Pitzer_Base(ActivityCoefficient_Pitzer_Base):
    solute = 'LiCl'
    concentration_range = (0, 6)
    coeffs = {
        'beta0': 0.1494,
        'beta1': 0.3074,
        'C_phi': 0.00359,
    }


class ActivityCoefficient_LiBr_Pitzer_Base(ActivityCoefficient_Pitzer_Base):
    solute = 'LiBr'
    concentration_range = (0, 2.5)
    coeffs = {
        'beta0': 0.1748,
        'beta1': 0.2547,
        'C_phi': 0.0053,
    }
