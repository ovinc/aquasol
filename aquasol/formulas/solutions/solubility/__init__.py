"""Activity coefficients of solutions"""

from .KCl import SolubilityFormulas_KCl
from .LiCl import SolubilityFormulas_LiCl
from .Na2SO4 import SolubilityFormulas_Na2SO4
from .Na2SO4_10H2O import SolubilityFormulas_Na2SO4_10H2O
from .NaCl import SolubilityFormulas_NaCl
from .NaCl_2H2O import SolubilityFormulas_NaCl_2H2O

SolubilityFormulas = (
    SolubilityFormulas_KCl +
    SolubilityFormulas_LiCl +
    SolubilityFormulas_Na2SO4 +
    SolubilityFormulas_Na2SO4_10H2O +
    SolubilityFormulas_NaCl +
    SolubilityFormulas_NaCl_2H2O
)
