from typing import Union

from Chatty.saveState.database import Connection

conn = None


def get_conn() -> Union[Connection, None]:
    return conn


def initialize_conn() -> None:
    global conn
    conn = Connection()
