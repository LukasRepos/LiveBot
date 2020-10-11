import calendar
from collections import deque
import datetime
from typing import Dict, Any

import nltk

agenda = {}
recurrent_events = {i: [] for i in range(7)}


def add_date(data: Dict[str, Any]) -> str:
    appointments = " ".join(nltk.sent_tokenize(data["document"])[1:])

    reference = data["reference"].lower()
    document = nltk.sent_tokenize(data["document"])[0].lower()
    if reference in document:
        date_string = document.split(reference)[1]
    else:
        return "Cannot understand the date :("

    patterns = [
        " %d %B, %Y.",    # 21 June, 2018
        " %d/%m/%Y.",     # 12/11/2018
        " %m/%d/%Y."      # 12/30/2018
    ]

    due_date = None
    for pattern in patterns:
        try:
            due_date = datetime.datetime.strptime(date_string, pattern)
            break
        except:
            continue

    if due_date is None:
        return "Date unknown... :("

    timestamp = calendar.timegm(due_date.timetuple())

    if timestamp not in agenda:
        agenda[timestamp] = []
    agenda[timestamp].append(appointments)

    return "Done sir"


def get_date(data: Dict[str, Any]) -> str:
    reference = data["reference"].lower()
    document = nltk.sent_tokenize(data["document"])[0].lower()
    if reference in document:
        date_string = document.split(reference)[1]
    else:
        return "Cannot understand the date :("

    patterns = [
        " %d %B, %Y.",    # 21 June, 2018
        " %d/%m/%Y.",     # 12/11/2018
        " %m/%d/%Y."      # 12/30/2018
    ]

    due_date = None
    for pattern in patterns:
        try:
            due_date = datetime.datetime.strptime(date_string, pattern)
            break
        except:
            continue

    if due_date is None:
        return "Date unknown... :("

    timestamp = calendar.timegm(due_date.timetuple())
    if timestamp not in agenda:
        return "Nothing! :D"

    msg = f"You have {len(agenda[timestamp])} things for tomorrow:"
    for appointment in agenda[timestamp]:
        msg += f"\n -> {appointment}"
    return msg


def add_tomorrow(data: Dict[str, Any]) -> str:
    appointments = " ".join(nltk.sent_tokenize(data["document"])[1:])
    due_date = datetime.datetime.today().date() + datetime.timedelta(days=1)
    timestamp = calendar.timegm(due_date.timetuple())

    if timestamp not in agenda:
        agenda[timestamp] = []
    agenda[timestamp].append(appointments)

    return "Done sir!"


def get_tomorrow(__: Dict[str, Any]) -> str:
    due_date = datetime.datetime.today().date() + datetime.timedelta(days=1)
    timestamp = calendar.timegm(due_date.timetuple())

    msg = "Nothing! :D"
    count = len(recurrent_events[due_date.weekday()])
    if timestamp in agenda:
        count += len(agenda[timestamp])
    if timestamp in agenda or len(recurrent_events[due_date.weekday()]) > 0:
        msg = f"You have {count} things for tomorrow:"

    if timestamp in agenda:
        for appointment in agenda[timestamp]:
            msg += f"\n -> {appointment}"
    if len(recurrent_events[due_date.weekday()]) > 0:
        for appointment in recurrent_events[due_date.weekday()]:
            msg += f"\n -> {appointment}"
    return msg


def add_recurrent(data: Dict[str, Any]) -> str:
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    appointments = " ".join(nltk.sent_tokenize(data["document"])[1:])

    reference = data["reference"].lower()
    document = nltk.sent_tokenize(data["document"])[0].lower()
    flag = False
    index = -1
    if reference in document:
        for i, weekday in enumerate(weekdays):
            if weekday in document:
                flag = True
                index = i
    else:
        return "Cannot understand the date :("

    if not flag:
        return "Cannot understand weekday :("

    recurrent_events[index].append(appointments)
    return "Done sir!"


def get_recurrent(data: Dict[str, Any]) -> str:
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    reference = data["reference"].lower()
    document = nltk.sent_tokenize(data["document"])[0].lower()
    flag = False
    index = -1
    if reference in document:
        for i, weekday in enumerate(weekdays):
            if weekday in document:
                flag = True
                index = i
    else:
        return "Cannot understand the date :("

    if not flag:
        return "Cannot understand weekday :("

    if len(recurrent_events[index]) == 0:
        return "Nothing sir! :D"
    else:
        msg = f"You have {len(recurrent_events[index])} things for {weekdays[index]}:"
        for appointment in recurrent_events[index]:
            msg += f"\n -> {appointment}"
        return msg


def debug(_: Dict[str, Any]) -> str:
    return str(agenda)
