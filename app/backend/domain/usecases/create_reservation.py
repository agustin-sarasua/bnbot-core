from abc import ABC, abstractmethod
from app.backend.infraestructure.repositories import ReservationRepository
from app.backend.domain.entities import Reservation

class CreateReservationUseCase:

    def __init__(self, repository: ReservationRepository):
        self.repository = repository

    def execute(self, reservation: Reservation):
        return self.repository.save(reservation)
        
