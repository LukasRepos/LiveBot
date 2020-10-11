import datetime
from math import inf
from pprint import pprint
from typing import Dict, Any

import requests


class Weather:
    def __init__(self, token: str):
        self.access_token = token

        self.BASE_URL = "https://api.openweathermap.org/data/2.5"

        self.FORECAST_URL = self.BASE_URL + "/forecast"

    def get_forecast(self, city: str, count: int = None) -> Dict[str, Any]:
        results = requests.get(self.FORECAST_URL, params={
            "units": "metric",
            "appid": self.access_token,
            "q": city,
            "cnt": count if count is not None else 40
        })

        if results.status_code == 200:
            res = results.json()
            return {"status": results.status_code, "data": res["list"], "cityInfo": res["city"]}
        else:
            return {"status": results.status_code}


if __name__ == "__main__":
    weatherAPI = Weather("4365e1c18a9a72fcaa98d9e97bc3df2f")
    forecasts = weatherAPI.get_forecast("aveiro")

    pprint(forecasts)

    current_day = datetime.datetime.today().day

    prev_day = None
    max_temp = -inf
    min_temp = inf
    for d in forecasts["data"]:
        date = datetime.datetime.utcfromtimestamp(d["dt"])

        if date.day == current_day:
            continue

        if prev_day is None:
            prev_day = date.day
            max_temp = d["main"]["temp_max"]
            min_temp = d["main"]["temp_min"]
            continue

        if prev_day == date.day:
            if max_temp < d["main"]["temp_max"]:
                max_temp = d["main"]["temp_max"]
            if min_temp > d["main"]["temp_min"]:
                min_temp = d["main"]["temp_min"]
        else:
            print(f"Tomorrow the max temp will be {max_temp} and the minimun will be {min_temp}")
            prev_day = date.day
            max_temp = -inf
            min_temp = inf
