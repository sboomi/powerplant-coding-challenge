from typing import List, Literal
from pydantic import BaseModel, Field


class Fuels(BaseModel):
    gas: float = Field(
        ..., example=13.4, title="Price of gas (euro/MWh)", alias="gas(euro/MWh)"
    )
    kerosine: float = Field(
        ...,
        example=50.8,
        title="Price of kerosine (euro/MWh)",
        alias="kerosine(euro/MWh)",
    )
    co2: float = Field(
        ...,
        example=20,
        title="Price of emission allowances (euro/ton)",
        alias="co2(euro/ton)",
    )
    wind: float = Field(
        ..., example=60, title="Percentage of wind (%)", ge=0, le=100, alias="wind(%)"
    )


class Powerplant(BaseModel):
    name: str = Field(..., example="gasfiredbig1", title="Name of the powerplant")
    type: Literal["gasfired", "turbojet", "windturbine"] = Field(
        ..., example="gasfired", title="Type of the powerplant"
    )
    efficiency: float = Field(
        ..., example=0.53, title="Fuel-to-energy efficiency conversion"
    )
    pmin: float = Field(..., example=100, title="Maximum amount of generated power")
    pmax: float = Field(..., example=460, title="Minimum amount of generated power")


class PowerplantPayload(BaseModel):
    load: float = Field(..., example=480, title="Amount of energy (MWh)")
    fuels: Fuels = Field(..., title="Powerplant fuel cost")
    powerplants: List[Powerplant] = Field(
        ..., title="Powerplants at disposal to generate load"
    )


class PowerplantDeliveryResponse(BaseModel):
    name: str = Field(..., example="windpark1", title="Name of the powerplant")
    p: float = Field(..., example=75, title="Power delivered (W)")
