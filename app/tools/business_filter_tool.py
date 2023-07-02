from datetime import datetime
from datetime import datetime, timedelta
from app.utils import Cache, read_json_from_s3, logger


class BusinessFilterTool:
    
    # properties_info_cache = Cache(-1)

    def run(
        self, 
        business_id: str, 
        location: str, 
        business_name: str,
        business_owner: str,
    ) -> dict:

        if business_id is not None and business_id != "":
            # Search from dynamoDB business_info
            pass
        
        if location is not None:
            pass
        pass


    def get_properties_availabe(self):
        result = self.properties_info_cache.get(self.assistant_number)        
        if result is None:
            result = self.load_properties_information()
        return result

    def load_business_information(self):
        # availability = read_json_from_s3("bnbot-bucket", f"availability_{self.assistant_number}.json")
        # self.properties_info_cache.set(self.assistant_number, availability)
        return availability