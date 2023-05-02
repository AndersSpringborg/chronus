import datetime
from dataclasses import dataclass


@dataclass
class SystemSample:
    timestamp: datetime.datetime = datetime.datetime.now()
    current_power_draw: float = 1.0
    cpu_power: float = 0.0
    cpu_temp: float = 0.0
