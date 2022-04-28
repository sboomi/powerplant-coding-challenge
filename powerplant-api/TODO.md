# TODO

## Calculate power

- Determine energy sources
- Determine $P_{min}$
- Determine $P_{max}$

The total load is a time series plotting time t and the power (in W)

## REST API

Routes:

- `/productionplan` accepting a POST request

Payload:

- `load`
- `fuels`
  - `gas`
  - `kerosine`
  - `co2`
- `powerplants`:
  - `name` (specified)
  - `type` (specified)
  - `efficiency` (specified)
  - `pmax` (specified)
  - `pmin` (specified)

Response:

- `name`
- `p`
