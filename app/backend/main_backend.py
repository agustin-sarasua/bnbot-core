import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
from fastapi import FastAPI, Form, Depends

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


from app.utils import logger

from app.backend.presentation.routers import reservation_router

from app.backend.domain.usecases import CreateReservationUseCase
from app.backend.infraestructure.repositories import ReservationRepository

def init_backend():
    logger.info("Inizializing Backend")
    DATABASE_URL = "postgresql://myuser:mypassword@db/mydatabase"
    engine = create_engine(DATABASE_URL)
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info("Database created successfully.")
    else:
        logger.info("Database already exists.")

    reservation_repository = ReservationRepository(DATABASE_URL)
    reservation_router.create_reservation_use_case = CreateReservationUseCase(reservation_repository)