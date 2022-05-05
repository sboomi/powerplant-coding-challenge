# Powerplant API

## Deployment

### Local

This project uses Python and Poetry. You need to have [Poetry (V1.1.x)](https://python-poetry.org/docs/#installation) enabled to use the project locally.

From now on you can launch the API like so:

```sh
# Install dependencies
poetry install

# Activate environment
poetry shell

# Launch app in development mode
poetry run run-app
```

### Docker

It's possible to build the app using Docker. To start the container, either use the following:

```shell
docker-compose up --build -d

# With makefile
make up
```

The app will be served on `http://localhost:8888/`. Thanks to FastAPI's ecosystem, you can access OpenAPI pages on these routes:

- `docs/` for Swagger API interface
- `redoc/` for Redoc documentation

## Routes

Aside from the main route, Powerplant API has one route called `/productionplan` that currently accepts a POST request with a payload for each active powerplant passed as an argument.

```sh
curl -X 'POST' \
  'http://localhost:8888/productionplan' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "load": 480,
  "fuels":
  {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    {
      "name": "gasfiredbig1",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "gasfiredbig2",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "gasfiredsomewhatsmaller",
      "type": "gasfired",
      "efficiency": 0.37,
      "pmin": 40,
      "pmax": 210
    },
    {
      "name": "tj1",
      "type": "turbojet",
      "efficiency": 0.3,
      "pmin": 0,
      "pmax": 16
    },
    {
      "name": "windpark1",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 150
    },
    {
      "name": "windpark2",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 36
    }
  ]
}
'
```

## Development

- `poetry run pytest` for tests
- `poetry run black` for formatting
