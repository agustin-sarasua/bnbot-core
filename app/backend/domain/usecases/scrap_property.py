from abc import ABC, abstractmethod
from app.backend.infraestructure.repositories import BusinessRepository
import scrapy

class ScrapPropertyUseCase:

    def __init__(self):
        pass

    def execute(self, http_link: str):

        pass
        # return self.repository.save(business)



if __name__ == '__main__':
    scaper = ScrapPropertyUseCase()
    result = scaper.execute(http_link ="https://www.booking.com/hotel/uy/casa-en-altos-arrayanes.html?lang=xu")
