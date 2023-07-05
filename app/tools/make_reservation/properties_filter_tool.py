from datetime import datetime
from datetime import datetime, timedelta
from app.utils import Cache, read_json_from_s3, logger


class PropertiesFilterTool:
    
    properties_info_cache = Cache(-1)

    def run(
        self, 
        bnbot_id: str,
        check_in_date: str, 
        check_out_date: str,
        num_guests: str,
    ) -> dict:
        num_guests = int(num_guests)
        if check_in_date is None or check_out_date is None or num_guests == 0:
            return dict()

        available_properties = self.load_properties_information(bnbot_id)
        return self._filter_properties(available_properties, check_in_date, check_out_date, num_guests)

    def _calculate_checkout_date(self, checkin_date, num_nights):
        checkin_datetime = datetime.strptime(checkin_date, '%Y-%m-%d')
        checkout_datetime = checkin_datetime + timedelta(days=num_nights)
        checkout_date = checkout_datetime.strftime('%Y-%m-%d')
        return checkout_date
    
    def _filter_properties(self, properties, checkin_date, checkout_date, num_guests):
        filtered_properties = {}
        for property_id, property_info in properties.items():
            availability = property_info.get('availability', [])
            for avail in availability:
                avail_checkin = avail.get('checkin_from')
                avail_checkout = avail.get('checkout_to')
                avail_capacity = int(property_info.get('max_guests', 0))
                if (
                    avail_checkin <= checkin_date
                    and avail_checkout >= checkout_date
                    and num_guests <= avail_capacity
                ):
                    # Remove multiple keys
                    del property_info["other_calendar_links"], property_info["availability"]
                    filtered_properties[property_id] = property_info
                    break  # Stop further iteration if a match is found
        return filtered_properties

    def get_properties_availabe(self, bnbot_id: str):
        result = self.properties_info_cache.get(bnbot_id)        
        if result is None:
            result = self.load_properties_information()
        return result

    def load_properties_information(self, bnbot_id: str):
        availability = read_json_from_s3("bnbot-availability", f"{bnbot_id}.json")
        self.properties_info_cache.set(bnbot_id, availability)
        return availability