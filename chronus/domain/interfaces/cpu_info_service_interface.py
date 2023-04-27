from typing import List

from dataclasses import dataclass


@dataclass
class CpuInfo:
    """ Returns the number of cores in the system. If the system has hyperthreading, this method should return the
    number of physical cores"""
    cpu: str = ""
    cores: int = 0
    threads_per_core: int = 1
    frequencies: List[float] = None


class CpuInfoServiceInterface:
    def get_cpu_info(self) -> CpuInfo:
        pass
