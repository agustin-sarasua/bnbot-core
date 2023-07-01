import os
from fastapi import FastAPI, Form, Depends

from app.utils import logger
import traceback

from app.backend.domain.usecases import CreateReservationUseCase
from app.backend.domain.entities import Reservation

from fastapi import APIRouter
from fastapi import Depends, FastAPI

reservation_api_router = APIRouter()

create_reservation_use_case: CreateReservationUseCase


@reservation_api_router.post("/reservation")
async def create_reservation(reservation: Reservation, 
                             usecase: CreateReservationUseCase=Depends(lambda:create_reservation_use_case)):
    try:
        # logger.info("create_reservation_use_case:", create_reservation_use_case)
        result = usecase.execute(reservation)
        response = {"statusCode": 200, "body": result}
        return response
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        response = {"statusCode": 500}
        return response

# Define the `routes` attribute as a list containing the reservation_router instance
routes = [create_reservation]    