from typing import List
from ..schemas import PowerplantPayload, PowerplantDeliveryResponse, Powerplant, Fuels


def get_energy_cost(
    powerplant: Powerplant, fuels: Fuels, emission_allowances: bool = False
) -> float:
    """Computes energy cost in €/MWh for a powerplant.

    Producing power using a turbojet uses kerosine while gasfired plants use
    gas as a fuel. Wind turbines aren't accounted for since they're only powered by
    the strength of the wind.

    If emission_allowances is switched on, the cost takes in account CO2 emissions
    from gasfired stations, which adds the price of CO2 in Euro per ton

    Parameters
    ----------
    powerplant : Powerplant
        Powerplant object to analyze from
    fuels : Fuels
        Fuels used by the powerplant
    emission_allowances : bool
        Takes CO2 into account. Dafaults to False.

    Returns
    -------
    float
        Energy cost in €/MWh. 0 by default.
    """
    if powerplant.type == "turbojet":
        return fuels.kerosine / powerplant.efficiency
    if powerplant.type == "gasfired":
        return (fuels.gas / powerplant.efficiency) + (
            fuels.co2 * 0.3 if emission_allowances else 0.0
        )

    return 0.0


def compute_power_delivery(
    pp_payload: PowerplantPayload, with_co2: bool = False
) -> List[PowerplantDeliveryResponse]:
    """Evaluates power delivery from each powerplant in the payload. The algorithm first evaluates
    which powerplants should be activated according to the merit-order, using energy price from
    `get_energy_cost`. It then deduces the power to use from the load.

    For energy-consuming powerplants, the algorithm deduces the power used among the three types of
    plants available :

    * If the plant is a `windturbine`, the power is immediately deduced from the remaining load with P_max and the
    percentage of wind available.
    * If the plant is an energy-consuming one, it will try to exploit the rest of the remaining load
    according to the power specifications.

    In case the remaining power is inferior to the minimal power allowed to start a powerplant production, the algorithm
    will take the necessary remainder from the previous plant in the list and add it to the next unit.

    It returns an array of powerplant deliveries with the `name` and the power in `p` MW per hour. The total sum
    is the initial load of the payload

    Parameters
    ----------
    pp_payload : PowerplantPayload
        Payload object containing the load, the plants and the available fuel + CO2 emission costs
    with_co2 : bool
        Option taking account of the CO2 emission calculation.

    Returns
    -------
    List[PowerplantDeliveryResponse]
        List of each powerplant from the payload delivering a power `p`
    """
    powerplant_response: List[PowerplantDeliveryResponse] = []
    remaining_load = pp_payload.load

    for idx_pplant, p_plant in enumerate(
        sorted(
            pp_payload.powerplants,
            key=lambda x: get_energy_cost(
                x, fuels=pp_payload.fuels, emission_allowances=with_co2
            ),
        )
    ):
        if remaining_load <= 0:
            power_used = 0.0
        else:
            if p_plant.type == "windturbine":
                power_used = p_plant.pmax * (pp_payload.fuels.wind / 100)
            else:
                power_used = min(p_plant.pmax, remaining_load)
                if (power_used - p_plant.pmin) <= 0:
                    powerplant_response[idx_pplant - 1].p -= abs(
                        power_used - p_plant.pmin
                    )
                    power_used = p_plant.pmin
        remaining_load -= power_used
        powerplant_response.append(
            PowerplantDeliveryResponse(name=p_plant.name, p=round(power_used))
        )

    return powerplant_response
