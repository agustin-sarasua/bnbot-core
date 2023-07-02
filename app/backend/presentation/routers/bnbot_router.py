import os
from fastapi import FastAPI, Form, Depends

from app.utils import logger
import traceback

from app.backend.domain.usecases import HandleMessageUseCase

from app.model import Message

from fastapi import APIRouter
from fastapi import Depends, FastAPI

bnbot_api_router = APIRouter()

handle_message_use_case: HandleMessageUseCase
    

@bnbot_api_router.post("/message")
async def handle_message(Body: str = Form(), 
                         To: str = Form(), 
                         From: str = Form(), 
                         ProfileName: str = Form(), 
                         usecase: HandleMessageUseCase=Depends(lambda:handle_message_use_case)):
    try:
        user_message = Message.user_message(Body)
        result = usecase.execute(user_message=user_message, customer_number=From)
        if result is not None:
            response = {"statusCode": 200, "body": result.text}
            return response
        return {"statusCode": 500}
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Exception {str(e)}")
        response = {"statusCode": 500}
        return response

# Define the `routes` attribute as a list containing the reservation_router instance
routes = [handle_message]    