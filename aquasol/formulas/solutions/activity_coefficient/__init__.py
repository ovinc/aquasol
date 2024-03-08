"""Activity coefficients of solutions"""

from .KCl import ActivityCoefficientFormulas_KCl
from .Na2SO4 import ActivityCoefficientFormulas_Na2SO4
from .NaCl import ActivityCoefficientFormulas_NaCl

ActivityCoefficientFormulas = (
    ActivityCoefficientFormulas_KCl +
    ActivityCoefficientFormulas_Na2SO4 +
    ActivityCoefficientFormulas_NaCl
)
