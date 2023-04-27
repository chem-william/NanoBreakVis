from dataclasses import dataclass
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from pydantic import (
    PositiveFloat,
    conlist,
    constr,
    condate,
)


class Solvent(BaseModel):
    """Dataclass for defining the solvent"""

    smiles: constr(strip_whitespace=True) = Field(
        description="A SMILES string of the solvent molecule"
    )
    supplier: Optional[constr(strip_whitespace=True)] = Field(
        "", description="The name of the supplier for the solvent, if applicable"
    )


class Electrode(BaseModel):
    """Dataclass for defining the electrodes"""

    material: constr(strip_whitespace=True) = Field(
        ..., description="The name of the material used for the electrode"
    )
    purity: PositiveFloat = Field(
        ..., description="The purity of the electrode material"
    )
    manufacturer: constr(strip_whitespace=True) = Field(
        ...,
        description="The name of the manufacturer of the material for the electrode",
    )
    diameter: PositiveFloat = Field(
        ...,
        description="The diameter of the electrode in millimeters. Units: millimeter (mm)",
    )


class Analyte(BaseModel):
    """Dataclass for defining the analyte"""

    smiles: constr(strip_whitespace=True) = Field(
        ..., description="A SMILES string of the analyte molecule"
    )
    concentration: PositiveFloat = Field(
        ...,
        description="The concentration of the analyte. Units: micromoles per liter (µM)",
    )


class Experiment(BaseModel):
    """Dataclass for defining an experiment"""

    # date: date = Field(
    #     ..., description="The date on which the experiment was conducted"
    # )
    experimentalists: conlist(constr(strip_whitespace=True)) = Field(
        description="The name(s) of the person(s) who conducted the experiment"
    )
    principal_investigators: conlist(constr(strip_whitespace=True)) = Field(
        description="The name(s) of the principal investigator(s) responsible for the experiment",
    )
    temperature: PositiveFloat = Field(
        ...,
        description="The temperature at which the experiment was conducted. Units: Kelvin (K)",
    )
    pressure: PositiveFloat = Field(
        ...,
        description="The pressure at which the experiment was conducted. Units: XXX (X)",
    )
    pulling_rate: PositiveFloat = Field(
        ...,
        description="The pulling rate used in the experiment. Units: nanometers per second (nm/s)",
    )
    acquisition_rate: PositiveFloat = Field(
        ..., description="The acquisition rate used in the experiment. Units: Hz"
    )
    method: constr(strip_whitespace=True) = Field(
        ..., description="The experimental method used. For example, STM-BJ, MCBJ, etc."
    )
    analyte: Analyte = Field(..., description="The molecule analyzed in the experiment")
    solvent: Solvent = Field(..., description="The solvent used in the experiment")
    bias_voltage: PositiveFloat = Field(
        ..., description="The bias voltage used in the experiment"
    )
    electrode: Electrode = Field(
        ..., description="The electrode used in the experiment"
    )
    procedure: str = Field(
        ...,
        description="A description of the experimental procedure used in the experiment",
    )
