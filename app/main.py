import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from fastapi import FastAPI, Form

from app.backend.presentation.routers import reservation_router, business_router, bnbot_router
from app.backend.main_backend import init_backend
import traceback

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_number = os.environ.get('TWILIO_NUMBER')
openai_token = os.environ.get('OPENAI_API_KEY')

# init_backend(account_sid, auth_token, twilio_number, openai_token)

app = FastAPI()

##### BACKEND #####
app.include_router(reservation_router.reservation_api_router)
app.include_router(business_router.business_api_router)
app.include_router(bnbot_router.bnbot_api_router)
##### BACKEND #####


@app.get("/")
async def root():
    return {"message": "Hello World 2"}    
