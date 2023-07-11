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
        # businesses = self.repository.list_all_businesses()
        # if load_business.bnbot_id is not None and load_business.bnbot_id != "":
        #     for business in businesses:
        #         if business.bnbot_id.lower() == load_business.bnbot_id.lower():
        #             return [business]
        # # logger.debug(f"Searching for {load_business.business_name} in {len(businesses)} businesses")
        # # logger.debug(f"******* Here are the businesses: {businesses}")
        # if load_business.business_name is not None and load_business.business_name != "":
        #     result = full_text_search(businesses, load_business.business_name, 'business_name')
        #     # logger.debug(f"******* Here are the results: {result}")
        #     return result[:3]
        # # logger.debug(f"******* For some reason it came here: {load_business}")
        return Business(business_id=user_id)

