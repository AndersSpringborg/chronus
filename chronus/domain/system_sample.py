from typing import TypedDict

import datetime
from dataclasses import dataclass


class CpuFreq(TypedDict):
    current: float
    min: float
    max: float


@dataclass
class SystemSample:
    timestamp: datetime.datetime = datetime.datetime.now()
    current_power_draw: float = 1.0
    cpu_power: float = 0.0
    cpu_temp: float = 0.0
    cpu_freq: [CpuFreq] = None
