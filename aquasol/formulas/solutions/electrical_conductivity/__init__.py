"""Electrical conductivity of solutions"""

from .KCl import ElectricalConductivity_KCl_Formulas
from .NaCl import ElectricalConductivity_NaCl_Formulas

ElectricalConductivityFormulas = (
    ElectricalConductivity_KCl_Formulas +
    ElectricalConductivity_NaCl_Formulas
)