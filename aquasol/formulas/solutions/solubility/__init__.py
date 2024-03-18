"""Activity coefficients of solutions"""

from .KCl import SolubilityFormulas_KCl
from .LiBr import SolubilityFormulas_LiBr
from .LiCl import SolubilityFormulas_LiCl
from .Na2SO4 import SolubilityFormulas_Na2SO4
from .NaCl import SolubilityFormulas_NaCl

SolubilityFormulas = (
    SolubilityFormulas_KCl +
    SolubilityFormulas_LiBr +
    SolubilityFormulas_LiCl +
    SolubilityFormulas_Na2SO4 +
    SolubilityFormulas_NaCl
)
