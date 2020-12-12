from typing import Dict, Any

import phonenumbers
from phonenumbers import carrier
from phonenumbers import geocoder


def phone_number_simple_info(data: Dict[str, Any]) -> str:
    phone_numbers = []

    for match in phonenumbers.PhoneNumberMatcher(data["document"], "PT"):
        phone_numbers.append((
            match.number,
            carrier.name_for_number(match.number, "en"),
            geocoder.country_name_for_number(match.number, "en")
        ))

    sub_msg = [f"the number {n[0].national_number} originally from {n[1]} located in {n[2]}" for n in phone_numbers]
    if len(phone_numbers) == 0:
        msg = "I didn't found a number to analyze!"
    elif len(phone_numbers) == 1:
        msg = f"The number found was {sub_msg[0]}"
    else:
        msg = f"The numbers found were: {', '.join(sub_msg[:-1])} and {sub_msg[-1]}."
    return msg
