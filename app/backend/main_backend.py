import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from fastapi import FastAPI, Form, Depends

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


from app.utils import logger

from app.backend.presentation.routers import reservation_router, business_router

from app.backend.domain.usecases import CreateReservationUseCase, CreateBusinessUseCase
from app.backend.infraestructure.repositories import ReservationRepository, BusinessRepository

def init_backend():
    logger.info("Inizializing Backend...")

    posgres_url = os.environ.get("DATABASE_URL")
    engine = create_engine(posgres_url)
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info("Database created successfully.")
    else:
        logger.info("Database already exists.")

    reservation_repository = ReservationRepository(posgres_url)
    reservation_router.create_reservation_use_case = CreateReservationUseCase(reservation_repository)


    dynamo_url = os.environ.get("DYNAMO_DB_URL")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = os.environ.get("REGION")
    # auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

    business_repository = BusinessRepository(aws_access_key_id, aws_secret_access_key, region, dynamo_url)
    business_router.create_business_use_case = CreateBusinessUseCase(business_repository)