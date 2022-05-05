from fastapi.testclient import TestClient

from powerplant_api.app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Thank you for using powerplant-api!"}


def test_production_plan_standard_response():
    response = client.post(
        "/productionplan",
        json={
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
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        {"name": "windpark1", "p": 90},
        {"name": "windpark2", "p": 22},
        {"name": "gasfiredbig1", "p": 368},
        {"name": "gasfiredbig2", "p": 0},
        {"name": "gasfiredsomewhatsmaller", "p": 0},
        {"name": "tj1", "p": 0},
    ]


def test_production_plan_no_wind():
    response = client.post(
        "/productionplan",
        json={
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
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        {"name": "windpark1", "p": 0},
        {"name": "windpark2", "p": 0},
        {"name": "gasfiredbig1", "p": 380.0},
        {"name": "gasfiredbig2", "p": 100},
        {"name": "gasfiredsomewhatsmaller", "p": 0},
        {"name": "tj1", "p": 0},
    ]


def test_production_plan_big_load():
    response = client.post(
        "/productionplan",
        json={
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
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        {"name": "windpark1", "p": 90},
        {"name": "windpark2", "p": 22},
        {"name": "gasfiredbig1", "p": 460},
        {"name": "gasfiredbig2", "p": 338},
        {"name": "gasfiredsomewhatsmaller", "p": 0},
        {"name": "tj1", "p": 0},
    ]
