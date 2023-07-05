from abc import ABC, abstractmethod
from app.backend.domain.entities.business import Property
from app.backend.infraestructure.repositories import ReservationRepository
from typing import List, Any

from app.utils import logger
import requests
from icalendar import Calendar
from typing import List
from datetime import date
from datetime import datetime, timedelta
import json
import boto3
import traceback

OPEN_DAYS = 30
BUCKET_NAME = "bnbot-calendar"

class UpdateCalendarUseCase:

    def __init__(self, repository: ReservationRepository):
        self.repository = repository

    # def read_icalendar_from_url(self, url):
    #     response = requests.get(url)
    #     response.raise_for_status()
    #     cal = Calendar.from_ical(response.text)
        
    #     events = []
    #     for component in cal.walk():
    #         if component.name == 'VEVENT':
    #             event = {}
    #             for key, value in component.items():
    #                 if key in ('DTSTART', 'DTEND', 'DTSTAMP'):
    #                     event[key] = self.parse_datetime(value.dt)
    #                 else:
    #                     event[key] = str(value)
    #             events.append(event)
        
    #     return events

    def save_dict_to_s3(self, dictionary, bucket_name, file_key):
        # Convert the dictionary to JSON
        json_data = json.dumps(dictionary)

        # Initialize the S3 client
        s3_client = boto3.client('s3')

        try:
            # Upload the JSON data to S3
            s3_client.put_object(Body=json_data, Bucket=bucket_name, Key=file_key)
            print(f"Successfully saved dictionary as JSON to S3 bucket: {bucket_name}, file key: {file_key}")
        except Exception as e:
            print(f"Error saving dictionary as JSON to S3: {str(e)}")


    def execute(self):
        logger.debug("Executing update_availability job...")
        
        businesses = self.repository.
        
        for business in businesses:
            business_availability = dict()
            
            for property in business.properties:
                availability = self.calculate_property_availability(property)
                prop_availability = property.dict() 
                prop_availability["availability"] = availability
                business_availability[property.property_id] = prop_availability

            logger.debug(f"Saving availability file for {business.bnbot_id}")
            self.save_dict_to_s3(business_availability, BUCKET_NAME, f"{business.bnbot_id}.json")

        



from icalendar import Calendar, Event, vText
from datetime import datetime
import pytz

def generate_ical_file(bookings, filename):
    """
    Generates an iCalendar file from a list of bookings.

    :param bookings: A list of bookings. Each booking is a dictionary with booking details.
    :param filename: Name of the output .ics file
    """
    # Create a Calendar
    cal = Calendar()
    cal.add('prodid', '-//Your Company//example.com//')
    cal.add('version', '2.0')

    # Time Zone definition
    tz = pytz.timezone("UTC")

    # Populate the calendar with bookings
    for booking in bookings:
        event = Event()

        # Check-in and check-out must be datetime objects
        # Convert the dates to datetime objects in UTC time zone
        event.add('dtstart', tz.localize(booking['check_in']))
        event.add('dtend', tz.localize(booking['check_out']))
        event.add('summary', booking['summary'])
        
        # Adding optional properties
        if 'description' in booking:
            event.add('description', booking['description'])
        if 'location' in booking:
            event.add('location', booking['location'])
        if 'attendee' in booking:
            event.add('attendee', booking['attendee'])
        if 'uid' in booking:
            event.add('uid', booking['uid'])
        if 'url' in booking:
            event.add('url', booking['url'])

        # Adding the event to the calendar
        cal.add_component(event)

    # Write the calendar to file
    with open(filename, 'wb') as f:
        f.write(cal.to_ical())
        
# Example usage:

bookings = [{
    'check_in': datetime(2023, 7, 6, 14, 0),
    'check_out': datetime(2023, 7, 7, 11, 0),
    'summary': 'Booking 1',
    'description': 'Conversation details here...',
    'location': 'Hotel XYZ, Address',
    'attendee': 'mailto:customer@example.com',
    'uid': 'reservation12345',
    'url': 'https://example.com/booking/12345'
}]

generate_ical_file(bookings, 'bookings.ics')
