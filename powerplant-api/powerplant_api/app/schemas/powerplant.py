from typing import List, Literal
from pydantic import BaseModel, Field


class Fuels(BaseModel):
    gas: float = Field(..., example=13.4, title="Price of gas (euro/MWh)", alias="gas(euro/MWh)")
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
    wind: float = Field(..., example=60, title="Percentage of wind (%)", ge=0, le=100, alias="wind(%)")


class Powerplant(BaseModel):
    name: str = Field(..., example="gasfiredbig1", title="Name of the powerplant")
    type: Literal["gasfired", "turbojet", "windturbine"] = Field(
        ..., example="gasfired", title="Type of the powerplant"
    )
    efficiency: float = Field(..., example=0.53, title="Fuel-to-energy efficiency conversion")
    pmin: float = Field(..., example=100, title="Maximum amount of generated power")
    pmax: float = Field(..., example=460, title="Minimum amount of generated power")


class PowerplantPayload(BaseModel):
    load: float = Field(..., example=480, title="Amount of energy (MWh)")
    fuels: Fuels = Field(..., title="Powerplant fuel cost")
    powerplants: List[Powerplant] = Field(..., title="Powerplants at disposal to generate load")

    class Config:
        schema_extra = {
            "example": {
                "load": 480,
                "fuels": {
                    "gas(euro/MWh)": 13.4,
                    "kerosine(euro/MWh)": 50.8,
                    "co2(euro/ton)": 20,
                    "wind(%)": 60,
                },
                "powerplants": [
                    {
                        "name": "gasfiredbig1",
                        "type": "gasfired",
                        "efficiency": 0.53,
                        "pmin": 100,
                        "pmax": 460,
                    },
                    {
                        "name": "gasfiredbig2",
                        "type": "gasfired",
                        "efficiency": 0.53,
                        "pmin": 100,
                        "pmax": 460,
                    },
                    {
                        "name": "gasfiredsomewhatsmaller",
                        "type": "gasfired",
                        "efficiency": 0.37,
                        "pmin": 40,
                        "pmax": 210,
                    },
                    {
                        "name": "tj1",
                        "type": "turbojet",
                        "efficiency": 0.3,
                        "pmin": 0,
                        "pmax": 16,
                    },
                    {
                        "name": "windpark1",
                        "type": "windturbine",
                        "efficiency": 1,
                        "pmin": 0,
                        "pmax": 150,
                    },
                    {
                        "name": "windpark2",
                        "type": "windturbine",
                        "efficiency": 1,
                        "pmin": 0,
                        "pmax": 36,
                    },
                ],
            }
        }


class PowerplantDeliveryResponse(BaseModel):
    name: str = Field(..., example="windpark1", title="Name of the powerplant")
    p: float = Field(..., example=75, title="Power delivered (W)")
