from abc import ABC, abstractmethod
from app.backend.infraestructure.repositories import BusinessRepository
from app.backend.domain.entities import LoadBusinesses, Business
from typing import List

from app.utils import logger

from collections import Counter
from typing import List

class UpdateAvailabilityUseCase:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self):
        logger.info("UpdateAvailabilityUseCase job executed!")
        businesses = self.repository.list_all_businesses()

        pass

