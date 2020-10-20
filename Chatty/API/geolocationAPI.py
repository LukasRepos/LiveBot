from pprint import pprint
from typing import Union

from geopy.geocoders import Nominatim
import geopy


class Geolocation:
    def __init__(self, user_agent="LiveBot"):
        self.api = Nominatim(user_agent=user_agent)

    def get_city_info(self, city: str) -> Union[None, geopy.location.Location]:
        return self.api.geocode(city)


if __name__ == "__main__":
    api = Geolocation()
    print(api.get_city_info(input("city>")))
