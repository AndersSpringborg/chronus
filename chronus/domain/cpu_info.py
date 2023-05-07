from typing import List

from dataclasses import dataclass


@dataclass
class CpuInfo:
    """Returns the number of cores in the system. If the system has hyperthreading, this method should return the
    number of physical cores"""

    name: str = ""
    cores: int = 0
    threads_per_core: int = 1
    frequencies: list[float] = None

    def __hash__(self):
        return hash((self.name, self.cores, self.threads_per_core, tuple(self.frequencies)))
