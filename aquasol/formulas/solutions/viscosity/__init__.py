"""Viscosity of solutions"""

from .NaCl import ViscosityFormulas_NaCl
from .KCl import ViscosityFormulas_KCl
from .LiCl import ViscosityFormulas_LiCl
from .glycerol import ViscosityFormulas_Glycerol

ViscosityFormulas = (
    ViscosityFormulas_NaCl +
    ViscosityFormulas_KCl +
    ViscosityFormulas_LiCl +
    ViscosityFormulas_Glycerol +
    ()
)
