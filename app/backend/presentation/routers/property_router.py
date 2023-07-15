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

property_api_router = APIRouter()

# load_availability_use_case: CreateBusinessUseCase

# @property_api_router.get("/properties/:property_id/availability")
# async def load_availability(usecase: UpdateAvailabilityUseCase=Depends(lambda:update_availability_use_case)):
#     try:
#         usecase.execute()
#         return JSONResponse(content="Availability Updated!", status_code=200)
#     except Exception as e:
#         traceback.print_exc()
#         logger.error(f"Exception {str(e)}")
#         return JSONResponse(content=str(e), status_code=500)