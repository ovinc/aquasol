"""Surface tension of solutions"""

from .CaCl2 import SurfaceTensionFormulas_CaCl2
from .KCl import SurfaceTensionFormulas_KCl
from .LiCl import SurfaceTensionFormulas_LiCl
from .MgCl2 import SurfaceTensionFormulas_MgCl2
from .Na2SO4 import SurfaceTensionFormulas_Na2SO4
from .NaCl import SurfaceTensionFormulas_NaCl

SurfaceTensionFormulas = (
    SurfaceTensionFormulas_CaCl2 +
    SurfaceTensionFormulas_KCl +
    SurfaceTensionFormulas_LiCl +
    SurfaceTensionFormulas_MgCl2 +
    SurfaceTensionFormulas_Na2SO4 +
    SurfaceTensionFormulas_NaCl
)
