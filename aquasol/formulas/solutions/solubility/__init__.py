"""Activity coefficients of solutions"""

from .KCl import SolubilityFormulas_KCl
from .LiCl import SolubilityFormulas_LiCl
from .Na2SO4 import SolubilityFormulas_Na2SO4
from .Na2SO4_10H2O import SolubilityFormulas_Na2SO4_10H2O
from .NaCl import SolubilityFormulas_NaCl

SolubilityFormulas = (
    SolubilityFormulas_KCl +
    SolubilityFormulas_LiCl +
    SolubilityFormulas_Na2SO4 +
    SolubilityFormulas_NaCl
)
