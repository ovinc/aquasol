"""Density of solutions"""

from .CaCl2 import Density_CaCl2_Formulas
from .KCl import Density_KCl_Formulas
from .KI import Density_KI_Formulas
from .LiCl import Density_LiCl_Formulas
from .MgCl2 import Density_MgCl2_Formulas
from .Na2SO4 import Density_Na2SO4_Formulas
from .NaCl import Density_NaCl_Formulas

DensityFormulas = (
    Density_CaCl2_Formulas +
    Density_KCl_Formulas +
    Density_KI_Formulas +
    Density_LiCl_Formulas +
    Density_MgCl2_Formulas +
    Density_Na2SO4_Formulas +
    Density_NaCl_Formulas
)
