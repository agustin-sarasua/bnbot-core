import requests
import json
import asyncio
from concurrent.futures import Future

from app.backend.domain.entities.business import LoadBusinesses
from app.backend.domain.entities.booking import Reservation
from app.backend.presentation.routers.business_router import list_businesses_sync
# from app.backend.presentation.routers.reservation_router import create_reservation_sync

class BackendAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        pass
        # self.base_url = "http://localhost:8080"

    def list_businesses(self, load_businesses):

        load_businesses = LoadBusinesses(
            bnbot_id=load_businesses.get("bnbot_id", ""),
            location=load_businesses.get("location", ""),
            business_name=load_businesses.get("business_name", ""),
            business_owner=load_businesses.get("business_owner", "")
        )

        response = list_businesses_sync(load_businesses)
        if response.status_code == 200:
            return json.loads(response.body.decode())
        else:
            return []
    
    def create_reservation(self, reservation: Reservation):

        # res
        pass