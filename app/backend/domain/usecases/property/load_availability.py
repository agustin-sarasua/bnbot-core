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

    def execute(self):

        # load business
        # get property by id
        # for each other calendar
        #   load calendar
        #   parse events
        #   add events to list

        # load own calendar
        # 

        pass