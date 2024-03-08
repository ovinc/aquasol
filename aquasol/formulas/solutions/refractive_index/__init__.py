"""Index of refraction of solutions"""

from .CaCl2 import RefractiveIndexFormulas_CaCl2
from .KCl import RefractiveIndexFormulas_KCl
from .NaCl import RefractiveIndexFormulas_NaCl

RefractiveIndexFormulas = (
    RefractiveIndexFormulas_CaCl2 +
    RefractiveIndexFormulas_KCl +
    RefractiveIndexFormulas_NaCl
)
