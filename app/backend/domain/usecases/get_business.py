from abc import ABC, abstractmethod
from app.backend.infraestructure.repositories import BusinessRepository
from app.backend.domain.entities import LoadBusinesses, Business
from typing import List

from app.utils import logger

from collections import Counter
from typing import List


class GetBusinessUseCase:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, user_id: str) -> Business:
        business = self.repository.load_by_user_id(user_id)
        if business is None:
            logger.debug(f"Creating new Business for user: {user_id}")
            business = self.repository.save(Business(user_id=user_id))
        
        return business

