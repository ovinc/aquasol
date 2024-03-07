"""Water activity of solutions"""

from .CaCl2 import WaterActivityFormulas_CaCl2
from .KCl import WaterActivityFormulas_KCl
from .LiCl import WaterActivityFormulas_LiCl
from .Na2SO4 import WaterActivityFormulas_Na2SO4
from .NaCl import WaterActivityFormulas_NaCl

WaterActivityFormulas = (
    WaterActivityFormulas_CaCl2 +
    WaterActivityFormulas_KCl +
    WaterActivityFormulas_LiCl +
    WaterActivityFormulas_Na2SO4 +
    WaterActivityFormulas_NaCl
)
