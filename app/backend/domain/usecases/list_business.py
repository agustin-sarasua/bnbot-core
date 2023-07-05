from abc import ABC, abstractmethod
from app.backend.infraestructure.repositories import BusinessRepository
from app.backend.domain.entities import LoadBusinesses, Business
from typing import List

from app.utils import logger

from collections import Counter
from typing import List

def full_text_search(businesses: List[Business], query: str, property_name: str) -> List[Business]:
    # Split the query into individual words
    query_words = query.lower().split()
    
    # Count the total occurrences of all words in the query for each business object's property
    counts = [sum(Counter(getattr(business, property_name, "").lower().split()).get(word, 0) for word in query_words) for business in businesses]

    # Zip together the Business objects and their counts
    businesses_with_counts = zip(businesses, counts)

    # Sort the Business objects based on the counts in descending order
    sorted_businesses_with_counts = sorted(businesses_with_counts, key=lambda x: x[1], reverse=True)

    # Extract the sorted Business objects
    sorted_businesses = [business for business, count in sorted_businesses_with_counts]

    return sorted_businesses

class ListBusinessUseCase:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, load_business: LoadBusinesses) -> List[Business]:
        businesses = self.repository.list_all_businesses()
        if load_business.bnbot_id is not None and load_business.bnbot_id != "":
            for business in businesses:
                if business.bnbot_id.lower() == load_business.bnbot_id.lower():
                    return [business]
        # logger.debug(f"Searching for {load_business.business_name} in {len(businesses)} businesses")
        # logger.debug(f"******* Here are the businesses: {businesses}")
        if load_business.business_name is not None and load_business.business_name != "":
            result = full_text_search(businesses, load_business.business_name, 'business_name')
            # logger.debug(f"******* Here are the results: {result}")
            return result[:3]
        # logger.debug(f"******* For some reason it came here: {load_business}")
        return []

