import datetime
from dataclasses import dataclass


@dataclass
class SystemSample:
    timestamp: datetime.datetime
    current_power_draw: float
    cpu_temp: float = 0.0
