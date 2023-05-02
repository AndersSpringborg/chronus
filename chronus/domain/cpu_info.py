from dataclasses import dataclass
from typing import List


@dataclass
class CpuInfo:
    """Returns the number of cores in the system. If the system has hyperthreading, this method should return the
    number of physical cores"""

    name: str = ""
    cores: int = 0
    threads_per_core: int = 1
    frequencies: List[float] = None
