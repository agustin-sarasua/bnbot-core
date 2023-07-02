import os
from fastapi import FastAPI, Form, Depends

from app.utils import logger
import traceback

from app.backend.domain.usecases import CreateBusinessUseCase, ListBusinessUseCase
from app.backend.domain.entities import Business, LoadBusinesses

from fastapi import APIRouter
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

business_api_router = APIRouter()

create_business_use_case: CreateBusinessUseCase
list_business_use_case: ListBusinessUseCase

@business_api_router.post("/business")
async def create_business(business: Business, 
                          usecase: CreateBusinessUseCase=Depends(lambda:create_business_use_case)):
    try:
        result = usecase.execute(business)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        response = {"statusCode": 500}
        return response


def list_businesses_sync(load_businesses: LoadBusinesses) -> JSONResponse:
    try:
        result = list_business_use_case.execute(load_businesses)
        business_dicts = [business.dict() for business in result]
        return JSONResponse(content=business_dicts, status_code=500)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)


@business_api_router.post("/list_business")
async def list_businesses(load_businesses: LoadBusinesses, 
                          usecase: ListBusinessUseCase=Depends(lambda:list_business_use_case)):
    try:
        result = usecase.execute(load_businesses)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)
    
# Define the `routes` attribute as a list containing the reservation_router instance
routes = [create_business, list_businesses]    