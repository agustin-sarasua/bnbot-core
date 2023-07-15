from abc import ABC, abstractmethod
from app.backend.infraestructure.repositories import *
from typing import List

from app.utils import logger
from icalendar import Calendar
from datetime import datetime
import boto3
from app.backend.domain.entities import Reservation

from icalendar import Calendar, Event
import pytz
import io

BUCKET_NAME = "bnbot-calendar"

class UpdateCalendarUseCase:

    def __init__(self, reservation_repository: ReservationRepository, business_repository: BusinessRepository):
        self.reservation_repository = reservation_repository
        self.business_repository = business_repository

    def write_reservations_to_ical(self, reservations: List[Reservation], bucket_name: str, file_name: str):
        # Create a Calendar object
        cal = Calendar()

        for reservation in reservations:
            # Create an Event for each reservation
            event = Event()

            # Set the details for the event
            event.add('summary', f"Reservation for {reservation.customer_name}")
            event.add('dtstart', datetime.strptime(reservation.check_in, "%Y-%m-%d").replace(tzinfo=pytz.UTC))
            event.add('dtend', datetime.strptime(reservation.check_out, "%Y-%m-%d").replace(tzinfo=pytz.UTC))
            event.add('description', f"Customer Name: {reservation.customer_name}\nCustomer Email: {reservation.customer_email}\nReservation Link: <Your Website URL>/reservations/{reservation.id}")

            # Add the event to the calendar
            cal.add_component(event)

        # Create an in-memory byte array file
        file_obj = io.BytesIO()
        file_obj.write(cal.to_ical())

        # Be sure to reset the file object's position to the start
        file_obj.seek(0)

        logger.debug("Uploading Calendar file to S3")
        # Upload the file to S3
        s3 = boto3.client('s3')
        s3.upload_fileobj(file_obj, bucket_name, file_name)


    def execute(self):
        logger.debug("Executing update_calendar job...")
        
        businesses = self.business_repository.list_all_businesses()
        for business in businesses:
            for property in business.properties:
                reservations = self.reservation_repository.load_by_property_id(property.property_id)
                self.write_reservations_to_ical(reservations, BUCKET_NAME, f"property_{property.property_id}.ical")