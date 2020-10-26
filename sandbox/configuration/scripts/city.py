from typing import Any, Dict

from Chatty.API.geolocationAPI import Geolocation

geolocationAPI = Geolocation()


def city_info(data: Dict[str, Any]) -> str:
    city = list(filter(lambda ent: ent.label_ == "GPE", data["NLP"].ents))
    if len(city) == 0:
        return "Could not recognize city... Try again"
    city = city[0].text

    city_info = geolocationAPI.get_city_info(city)
    return f"The complete address is {city_info.address} and it is located at the latitude {city_info.latitude} and longitude {city_info.longitude}"
