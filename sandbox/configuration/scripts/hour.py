from datetime import datetime
from typing import Dict, Any


def response(__: Dict[str, Any]) -> str:
    time = datetime.today()

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    hour = time.hour
    minute = time.minute
    second = time.second

    day = time.day
    month = time.month
    year = time.year

    return f"Today is day {day} of {months[month]} of the year {year} and the hours are exactly {hour} hours, {minute} minutes and {second} second{'s' if second > 1 else ''}."
