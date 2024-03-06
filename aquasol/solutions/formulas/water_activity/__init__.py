"""Water activity"""

from .NaCl import AwFormulas_NaCl
from ....general import SolutionProperty


class WaterActivity(SolutionProperty):
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
    Formulas = AwFormulas_NaCl
    quantity = 'water activity'
    unit = '[-]'
