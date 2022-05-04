from powerplant_api.app.energy_ops import get_energy_cost
from powerplant_api.app.schemas import PowerplantPayload, PowerplantDeliveryResponse, Powerplant, Fuels

example_payload_1 = PowerplantPayload(
    **{
        "load": 480,
        "fuels": {"gas(euro/MWh)": 13.4, "kerosine(euro/MWh)": 50.8, "co2(euro/ton)": 20, "wind(%)": 60},
        "powerplants": [
            {"name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
            {"name": "gasfiredbig2", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
            {"name": "gasfiredsomewhatsmaller", "type": "gasfired", "efficiency": 0.37, "pmin": 40, "pmax": 210},
            {"name": "tj1", "type": "turbojet", "efficiency": 0.3, "pmin": 0, "pmax": 16},
            {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150},
            {"name": "windpark2", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 36},
        ],
    }
)

example_payload_2 = PowerplantPayload(
    **{
        "load": 480,
        "fuels": {"gas(euro/MWh)": 13.4, "kerosine(euro/MWh)": 50.8, "co2(euro/ton)": 20, "wind(%)": 0},
        "powerplants": [
            {"name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
            {"name": "gasfiredbig2", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
            {"name": "gasfiredsomewhatsmaller", "type": "gasfired", "efficiency": 0.37, "pmin": 40, "pmax": 210},
            {"name": "tj1", "type": "turbojet", "efficiency": 0.3, "pmin": 0, "pmax": 16},
            {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150},
            {"name": "windpark2", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 36},
        ],
    }
)

example_payload_3 = PowerplantPayload(
    **{
        "load": 910,
        "fuels": {"gas(euro/MWh)": 13.4, "kerosine(euro/MWh)": 50.8, "co2(euro/ton)": 20, "wind(%)": 60},
        "powerplants": [
            {"name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
            {"name": "gasfiredbig2", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
            {"name": "gasfiredsomewhatsmaller", "type": "gasfired", "efficiency": 0.37, "pmin": 40, "pmax": 210},
            {"name": "tj1", "type": "turbojet", "efficiency": 0.3, "pmin": 0, "pmax": 16},
            {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150},
            {"name": "windpark2", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 36},
        ],
    }
)

example_response = [
    PowerplantDeliveryResponse(**{"name": "windpark1", "p": 75}),
    PowerplantDeliveryResponse(**{"name": "windpark2", "p": 18}),
    PowerplantDeliveryResponse(**{"name": "gasfiredbig1", "p": 200}),
    PowerplantDeliveryResponse(**{"name": "gasfiredbig1", "p": 0}),
    PowerplantDeliveryResponse(**{"name": "tj1", "p": 0}),
    PowerplantDeliveryResponse(**{"name": "tj2", "p": 0}),
]


def test_simple_generation_cost_gas():
    example_powerplant = Powerplant(name="gasfired1", type="gasfired", efficiency=0.5, pmin=20, pmax=200)
    example_fuel = Fuels(gas=6, kerosine=12, co2=20, wind=10)

    actual_energy_price = get_energy_cost(example_powerplant, example_fuel)
    expected_energy_price = 12

    assert actual_energy_price == expected_energy_price, f"Expected {expected_energy_price}. Got {actual_energy_price}"
