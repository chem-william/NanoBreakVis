from dataclasses import dataclass
from datetime import date
from typing import Optional
from pydantic import BaseModel
from pydantic import (
    PositiveFloat,
    constr,
    condate,
)


class Solvent(BaseModel):
    """Dataclass for defining the solvent"""

    smiles: constr(strip_whitespace=True)
    supplier: Optional[constr(strip_whitespace=True)]


class Electrode(BaseModel):
    """Dataclass for defining the electrodes"""

    material: constr(strip_whitespace=True)
    purity: PositiveFloat
    manufacturer: constr(strip_whitespace=True)
    diameter: PositiveFloat  # units: millimeter (mm)


class Analyte(BaseModel):
    """Dataclass for defining the analyte"""

    smiles: constr(strip_whitespace=True)
    concentration: PositiveFloat  # micromolar per liter (µM)


class Experiment(BaseModel):
    """Dataclass for defining an experiment"""

    date: date
    name_experimentalist: constr(strip_whitespace=True)
    name_principal_investigator: constr(strip_whitespace=True)
    method: constr(strip_whitespace=True)
    analyte: Analyte
    temperature: PositiveFloat  # units: kelvin (K)
    pressure: PositiveFloat
    solvent: Solvent
    bias_voltage: PositiveFloat
    acquisition_rate: PositiveFloat  # units: Hz
    pulling_rate: PositiveFloat  # units: nanometer per second (nm/s)
    electrode: Electrode
    procedure: str
