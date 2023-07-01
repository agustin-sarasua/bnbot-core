from abc import ABC, abstractmethod
from app.backend.infraestructure.repositories import BusinessRepository
from app.backend.domain.entities import Business

class ScrapPropertyUseCase:

    def __init__(self):
        pass

    def execute(self, http_link: str = "https://www.booking.com/hotel/uy/casa-en-altos-arrayanes.html?lang=xu"):

        pass
        # return self.repository.save(business)
        
