import os
from fastapi import FastAPI, Form, Depends

from app.utils import logger
import traceback

from app.backend.domain.usecases import CreateBusinessUseCase, ListBusinessUseCase, UpdateAvailabilityUseCase, GetBusinessUseCase
from app.backend.domain.entities import Business, LoadBusinesses

from app.backend.infraestructure.services import validate_token
from app.backend.domain.entities import TokenData

from fastapi import APIRouter
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

business_api_router = APIRouter()

create_business_use_case: CreateBusinessUseCase
list_business_use_case: ListBusinessUseCase
update_availability_use_case: UpdateAvailabilityUseCase
get_business_use_case: GetBusinessUseCase

@business_api_router.get("/update_availability")
async def update_availability(usecase: UpdateAvailabilityUseCase=Depends(lambda:update_availability_use_case)):
    try:
        usecase.execute()
        return JSONResponse(content="Availability Updated!", status_code=200)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)

@business_api_router.post("/business")
async def create_business(business: Business, 
                          usecase: CreateBusinessUseCase=Depends(lambda:create_business_use_case)):
    try:
        result = usecase.execute(business)
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)


def list_businesses_sync(load_businesses: LoadBusinesses) -> JSONResponse:
    try:
        result = list_business_use_case.execute(load_businesses)
        business_dicts = [business.dict() for business in result]
        return JSONResponse(content=business_dicts, status_code=200)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)


@business_api_router.post("/list_business")
async def list_businesses(load_businesses: LoadBusinesses, 
                          usecase: ListBusinessUseCase=Depends(lambda:list_business_use_case)):
    try:
        result = usecase.execute(load_businesses)
        business_dicts = [business.dict() for business in result]
        return JSONResponse(content=business_dicts, status_code=200)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)
    
@business_api_router.get("/business")
async def get_business(token: TokenData = Depends(validate_token),
                        usecase: GetBusinessUseCase=Depends(lambda:get_business_use_case)):
    try:
        logger.debug(f"Token: {token.sub}")
        result = usecase.execute(token.sub)
        return JSONResponse(content=result.dict(), status_code=200)
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        return JSONResponse(content=str(e), status_code=500)    
    
# Define the `routes` attribute as a list containing the reservation_router instance
routes = [create_business, list_businesses, get_business]    