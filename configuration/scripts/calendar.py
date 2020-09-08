import calendar
from collections import deque
import datetime

import nltk

agenda = {}


def add_tomorrow(_: deque, doc: str, ___: str) -> str:
    appointment = " ".join(nltk.sent_tokenize(doc)[1:])
    due_date = datetime.datetime.today().date() + datetime.timedelta(days=1)
    timestamp = calendar.timegm(due_date.timetuple())

    if timestamp not in agenda:
        agenda[timestamp] = []
    agenda[timestamp].append(appointment)

    return "Done sir!"


def get_tomorrow(_: deque, __: str, ___: str) -> str:
    due_date = datetime.datetime.today().date() + datetime.timedelta(days=1)
    timestamp = calendar.timegm(due_date.timetuple())
    if timestamp in agenda:
        msg = f"You have {len(agenda[timestamp])} things for tomorrow:"
        for appointment in agenda[timestamp]:
            msg += f"\n -> {appointment}"
        return msg
    return "Nothing!"


def debug(_: deque, __: str, ___: str) -> str:
    return str(agenda)
