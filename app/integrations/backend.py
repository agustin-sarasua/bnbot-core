import requests
import json

class BackendAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def list_businesses(self, load_businesses):
        url = f"{self.base_url}/list_business"
        try:
            response = requests.post(url, json=load_businesses)
            if response.status_code == 200:
                return response.json()
            else:
                # You might want to handle different status codes here (e.g. 400, 403, etc.)
                return {"error": "Failed to fetch data", "status_code": response.status_code}
        except requests.RequestException as e:
            return {"error": str(e)}