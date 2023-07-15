from abc import ABC, abstractmethod
from app.backend.domain.entities.business import Property
from app.backend.infraestructure.repositories import BusinessRepository
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
BUCKET_NAME = "bnbot-availability"

class UpdateAvailabilityUseCase:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def parse_datetime(self, value):
        if isinstance(value, datetime):
            return value
        elif isinstance(value, str):
            return datetime.fromisoformat(value)
        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        else:
            raise ValueError(f"Invalid datetime value: {value}")

    def read_icalendar_from_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        cal = Calendar.from_ical(response.text)
        
        events = []
        for component in cal.walk():
            if component.name == 'VEVENT':
                event = {}
                for key, value in component.items():
                    if key in ('DTSTART', 'DTEND', 'DTSTAMP'):
                        event[key] = self.parse_datetime(value.dt)
                    else:
                        event[key] = str(value)
                events.append(event)
        
        return events
    
    def get_date_range(self, start_date, end_date):
        delta = end_date - start_date
        num_days = delta.days

        dates = []
        for day in range(num_days + 1):
            dt = start_date + timedelta(days=day)
            dates.append(dt)

        return dates

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


    def calculate_availability_from_events(self, event_list, open_days=OPEN_DAYS):

        last_start_date = (datetime.now() + timedelta(days=1)).date()
        last_end_date = (datetime.now() + timedelta(days=open_days)).date()

        availability = []

        if len(event_list) == 0:
            availability.append({"checkin_from": f"{last_start_date}", "checkout_to": f"{last_end_date}", "num_nights": f"{open_days}"})
            return availability

        # Print the details of each event
        for event in event_list:
            print(event)

            # Example usage
            print(f"last_start_date {last_start_date}")
            start = last_start_date
            end = min(event['DTSTART'].date(), last_end_date)

            if event['DTSTART'].date() > last_end_date:
                break

            datetime_range = self.get_date_range(start, end)

            num_nights = len(datetime_range)
            print(f"start_date: {start} for num_nights: {num_nights}")

            availability.append({"checkin_from": f"{start}", "checkout_to": f"{start + timedelta(days=num_nights)}", "num_nights": f"{num_nights}"})
            last_start_date = event['DTEND'].date()
            print(f"last_start_date {last_start_date}")

        if last_start_date < last_end_date:
            datetime_range = self.get_date_range(last_start_date, last_end_date)
            availability.append({"checkin_from": f"{last_start_date}", "checkout_to": f"{last_end_date}", "num_nights": f"{len(datetime_range)}"})

        return availability
    
    def calculate_property_availability(self, property: Property) -> List[Any]:
        property_events = []
        try:
            for calendar_link in property.other_calendar_links:
                logger.debug(f"Loading calendar for {property.name} from {calendar_link}")
                
                events_list = self.read_icalendar_from_url(calendar_link)
                property_events = property_events + events_list

            availability = self.calculate_availability_from_events(events_list, open_days=OPEN_DAYS)
            return availability
        except Exception as e:
            traceback.print_exc()
            logger.error(f"Exception calculating availability for property {property.property_id}, returning []")
            return []

    def execute(self):
        logger.debug("Executing update_availability job...")
        
        businesses = self.repository.list_all_businesses()
        
        for business in businesses:
            business_availability = dict()
            
            for property in business.properties:
                availability = self.calculate_property_availability(property)
                prop_availability = property.dict() 
                prop_availability["availability"] = availability
                business_availability[property.property_id] = prop_availability

            logger.debug(f"Saving availability file for {business.bnbot_id}")
            self.save_dict_to_s3(business_availability, BUCKET_NAME, f"{business.bnbot_id}.json")

        

