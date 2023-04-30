import datetime
from datetime import datetime


def create_datatime_with_seconds(seconds):
    return datetime(year=2020, month=1, day=1, hour=0, minute=0, second=seconds)


def datetime_from_string(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
