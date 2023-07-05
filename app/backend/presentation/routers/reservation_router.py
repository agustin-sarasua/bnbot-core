import os
from fastapi import FastAPI, Form, Depends

from app.utils import logger
import traceback

from app.backend.domain.usecases import CreateReservationUseCase
from app.backend.domain.entities import Reservation

from fastapi import APIRouter
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

reservation_api_router = APIRouter()

create_reservation_use_case: CreateReservationUseCase


def create_reservation_sync(reservation: Reservation) -> JSONResponse:
    try:
        result = create_reservation_use_case.execute(reservation)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)

@reservation_api_router.post("/reservation")
async def create_reservation(reservation: Reservation, 
                             usecase: CreateReservationUseCase=Depends(lambda:create_reservation_use_case)):
    try:
        # logger.info("create_reservation_use_case:", create_reservation_use_case)
        result = usecase.execute(reservation)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)

# Define the `routes` attribute as a list containing the reservation_router instance
routes = [create_reservation]    