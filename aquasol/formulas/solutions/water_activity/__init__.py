"""Water activity of solutions"""

from .CaCl2 import WaterActivityFormulas_CaCl2
from .KCl import WaterActivityFormulas_KCl
from .LiBr import WaterActivityFormulas_LiBr
from .LiCl import WaterActivityFormulas_LiCl
from .Na2SO4 import WaterActivityFormulas_Na2SO4
from .NaCl import WaterActivityFormulas_NaCl
from .glycerol import WaterActivityFormulas_Glycerol

WaterActivityFormulas = (
    WaterActivityFormulas_CaCl2 +
    WaterActivityFormulas_KCl +
    WaterActivityFormulas_LiBr +
    WaterActivityFormulas_LiCl +
    WaterActivityFormulas_Na2SO4 +
    WaterActivityFormulas_NaCl +
    WaterActivityFormulas_Glycerol
)
