import datetime
import json
import os
import pathlib
import string
from collections import deque
from math import inf
from pprint import pprint


from Chatty.API.weatherAPI import Weather

with open("../sandbox/configuration/APIKEYS.json") as f:
    keys = json.load(f)

weather_api_key = keys["WEATHER"]


def forecast(_: deque, doc: str, reference: str) -> str:
    try:
        city = doc.split(reference)[1]
    except IndexError:
        return "Did not understood city"

    for punct in string.punctuation:
        city = city.replace(punct, "")

    weather_api = Weather(weather_api_key)
    forecasts = weather_api.get_forecast(city)
    if forecasts["status"] == 404:
        return "Did not understood city"

    tomorrow = datetime.datetime.today().date() + datetime.timedelta(days=1)

    max_temp = -inf
    max_temp_hour = 0

    min_temp = inf
    min_temp_hour = 0
    for d in forecasts["data"]:
        date = datetime.datetime.utcfromtimestamp(d["dt"])

        if date.day == tomorrow.day:
            if max_temp < d["main"]["temp_max"]:
                max_temp = d["main"]["temp_max"]
                max_temp_hour = date.hour
            if min_temp > d["main"]["temp_min"]:
                min_temp = d["main"]["temp_min"]
                min_temp_hour = date.hour
        else:
            continue
    return f"Tomorrow the max temp will be {max_temp}ºC at {max_temp_hour}h and the minimum will be {min_temp}ªC at {min_temp_hour}h."
