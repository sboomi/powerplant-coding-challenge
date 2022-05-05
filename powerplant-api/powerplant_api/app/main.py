from typing import Any, List, Optional

from fastapi import FastAPI, HTTPException, status

from .schemas import PowerplantDeliveryResponse, PowerplantPayload
from .energy_management import compute_power_delivery

app = FastAPI(title="Powerplant API")


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    """
    Greets user with a warm welcome message 😊
    """
    return {"message": "Thank you for using powerplant-api!"}


@app.post(
    "/productionplan",
    response_model=List[PowerplantDeliveryResponse],
    status_code=status.HTTP_200_OK,
)
def production_plan(pp_payload: PowerplantPayload) -> Any:
    """
    Computes the power needed for each powerplant as a list with the following:

    - **name**: name of the powerplant
    - **p**: power in W
    \f
    :param PowerplantPayload: Powerplant energy load.
    """
    power_delivery = compute_power_delivery(pp_payload)

    if sum([power_el.p for power_el in power_delivery]) != pp_payload.load:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The total must be equal to the load. Add more powerplants."
        )

    return power_delivery
