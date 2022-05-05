from powerplant_api.app.energy_management.energy_ops import (
    get_energy_cost,
    compute_power_delivery,
)
from powerplant_api.app.schemas import (
    PowerplantPayload,
    PowerplantDeliveryResponse,
    Powerplant,
    Fuels,
)

example_payload_1 = PowerplantPayload(
    **{
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
)

example_payload_2 = PowerplantPayload(
    **{
        "load": 480,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 0,
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
)

example_payload_3 = PowerplantPayload(
    **{
        "load": 910,
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
    example_efficiency = 0.5
    example_fuel_gas = 6

    actual_energy_price = example_fuel_gas / example_efficiency
    expected_energy_price = 12

    assert (
        actual_energy_price == expected_energy_price
    ), f"Expected {expected_energy_price}. Got {actual_energy_price}"


def test_order_set_of_powerplants_by_energy_cost():
    expected_result = [
        ("gasfiredbig1", 25.28),
        ("gasfiredbig2", 25.28),
        ("gasfiredsomewhatsmaller", 36.22),
        ("tj1", 169.33),
        ("windpark1", 0.0),
        ("windpark2", 0.0),
    ]

    actual_result = [
        (p_plant.name, round(get_energy_cost(p_plant, example_payload_1.fuels), 2))
        for p_plant in example_payload_1.powerplants
    ]

    assert (
        expected_result == actual_result
    ), f"Expected {expected_result}. Got {actual_result}"


def test_order_set_of_powerplants_by_total_cost():
    expected_result = [
        ("gasfiredbig1", 31.28),
        ("gasfiredbig2", 31.28),
        ("gasfiredsomewhatsmaller", 42.22),
        ("tj1", 169.33),
        ("windpark1", 0.0),
        ("windpark2", 0.0),
    ]

    actual_result = [
        (
            p_plant.name,
            round(
                get_energy_cost(
                    p_plant, example_payload_1.fuels, emission_allowances=True
                ),
                2,
            ),
        )
        for p_plant in example_payload_1.powerplants
    ]

    assert (
        expected_result == actual_result
    ), f"Expected {expected_result}. Got {actual_result}"


def test_compute_power_delivery_simple_configuration():
    expected_result = [
        PowerplantDeliveryResponse(**{"name": "windpark1", "p": 90}),
        PowerplantDeliveryResponse(**{"name": "windpark2", "p": 22}),
        PowerplantDeliveryResponse(**{"name": "gasfiredbig1", "p": 368}),
        PowerplantDeliveryResponse(**{"name": "gasfiredbig2", "p": 0}),
        PowerplantDeliveryResponse(**{"name": "gasfiredsomewhatsmaller", "p": 0}),
        PowerplantDeliveryResponse(**{"name": "tj1", "p": 0}),
    ]

    actual_result = compute_power_delivery(example_payload_1)
    actual_total_load = sum([p_plant.p for p_plant in actual_result])

    assert (
        example_payload_1.load == actual_total_load
    ), f"Expected {example_payload_1.load}. Got {actual_total_load}"
    assert (
        expected_result == actual_result
    ), f"Expected {expected_result}. Got {actual_result}"


def test_compute_power_delivery_no_wind():
    expected_result = [
        PowerplantDeliveryResponse(**{"name": "windpark1", "p": 0}),
        PowerplantDeliveryResponse(**{"name": "windpark2", "p": 0}),
        PowerplantDeliveryResponse(**{"name": "gasfiredbig1", "p": 380.0}),
        PowerplantDeliveryResponse(**{"name": "gasfiredbig2", "p": 100}),
        PowerplantDeliveryResponse(**{"name": "gasfiredsomewhatsmaller", "p": 0}),
        PowerplantDeliveryResponse(**{"name": "tj1", "p": 0}),
    ]

    actual_result = compute_power_delivery(example_payload_2)
    actual_total_load = sum([p_plant.p for p_plant in actual_result])
    assert (
        example_payload_2.load == actual_total_load
    ), f"Expected {example_payload_2.load}. Got {actual_total_load}"
    assert (
        expected_result == actual_result
    ), f"Expected {expected_result}. Got {actual_result}"


def test_compute_power_delivery_big_load():
    expected_result = [
        PowerplantDeliveryResponse(**{"name": "windpark1", "p": 90}),
        PowerplantDeliveryResponse(**{"name": "windpark2", "p": 22}),
        PowerplantDeliveryResponse(**{"name": "gasfiredbig1", "p": 460}),
        PowerplantDeliveryResponse(**{"name": "gasfiredbig2", "p": 338}),
        PowerplantDeliveryResponse(**{"name": "gasfiredsomewhatsmaller", "p": 0}),
        PowerplantDeliveryResponse(**{"name": "tj1", "p": 0}),
    ]

    actual_result = compute_power_delivery(example_payload_3)
    actual_total_load = sum([p_plant.p for p_plant in actual_result])
    assert (
        example_payload_3.load == actual_total_load
    ), f"Expected {example_payload_3.load}. Got {actual_total_load}"
    assert (
        expected_result == actual_result
    ), f"Expected {expected_result}. Got {actual_result}"
