from abc import ABC, abstractmethod
from app.backend.infraestructure.repositories import BusinessRepository
from app.backend.domain.entities import Business

class CreateBusinessUseCase:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, business: Business):
        return self.repository.save(business)
        
