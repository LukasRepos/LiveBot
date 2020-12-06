import random
from typing import Any, Dict

from Chatty.API.countryAPI import Country
from Chatty.API.geolocationAPI import Geolocation

geolocationAPI = Geolocation()
countryAPI = Country()


def city_info(data: Dict[str, Any]) -> str:
    cities = list(filter(lambda ent: ent.label_ == "GPE", data["NLP"].ents))
    if len(cities) == 0:
        return "Could not recognize city... Try again"
    city = cities[0].text

    city_info = geolocationAPI.get_city_info(city)
    return f"The complete address is {city_info.address} and it is located at the latitude {city_info.latitude} and longitude {city_info.longitude}"


def country_info(data: Dict[str, Any]) -> str:
    countries = list(filter(lambda ent: ent.label_ == "GPE", data["NLP"].ents))
    if len(countries) == 0:
        return "Could not recognize city... Try again"
    country = countries[0].text

    info = countryAPI.get_info(country)

    # information extraction
    alt_spellings = info["response"]["altSpellings"]                      # array check for length
    country_name = info["response"]["name"]
    capital = info["response"]["capital"]
    languages = [lang["name"] for lang in info["response"]["languages"]]  # safe to assume that length is greater or equal to 1
    population = info["response"]["population"]
    region = info["response"]["region"]

    # creation of messages for each piece of information
    if len(alt_spellings) == 0 or (alt_spellings[0].isupper() and len(alt_spellings) == 1):
        alt_spellings_str = f"{country_name.capitalize()} has no other nicknames."
    else:
        alt_spellings_str = f"{country_name.capitalize()} is also known as {', '.join(alt_spellings[1:])}."

    capital_str = f"{country_name.capitalize()}'s capital is {capital}."

    if len(languages) == 1:
        languages_str = f"The only language spoken in this country is {languages[0]}."
    else:
        languages_str = f"The languages spoken are {', '.join(languages)}."

    population_str = f"The population in the previous census is {population}."

    region_str = f"This country is located in the {region}."

    msg_parts = [alt_spellings_str, capital_str, languages_str, population_str, region_str]
    random.shuffle(msg_parts)
    msg = " ".join(msg_parts)

    return msg
