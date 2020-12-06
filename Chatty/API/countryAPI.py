from typing import Any, Dict

import requests


class Country:
    def __init__(self):
        self.base_url = "https://restcountries.eu/rest/v2"

    def get_info(self, country: str) -> Dict[str, Any]:
        url = "{:s}/{:s}/{:s}".format(self.base_url, "name", country)
        results = requests.request("GET", url)

        if results.status_code == 200:
            res = results.json()[0]
            return {"status": 200, "response": res}
        return {"status": results.status_code}

