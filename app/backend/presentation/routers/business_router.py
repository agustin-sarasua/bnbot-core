import os
from fastapi import FastAPI, Form, Depends

from app.utils import logger
import traceback

from app.backend.domain.usecases import CreateBusinessUseCase
from app.backend.domain.entities import Business

from fastapi import APIRouter
from fastapi import Depends, FastAPI

business_api_router = APIRouter()

create_business_use_case: CreateBusinessUseCase


@business_api_router.post("/business")
async def create_business(business: Business, 
                          usecase: CreateBusinessUseCase=Depends(lambda:create_business_use_case)):
    try:
        result = usecase.execute(business)
        response = {"statusCode": 200, "body": result}
        return response
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        response = {"statusCode": 500}
        return response

# Define the `routes` attribute as a list containing the reservation_router instance
routes = [create_business]    