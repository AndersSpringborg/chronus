from typing import List

from dataclasses import dataclass


@dataclass
class CpuInfo:
    cpu: str
    pass


class CpuInfoServiceInterface:
    def get_cpu_info(self) -> CpuInfo:
        pass

    def get_frequencies(self) -> List[float]:
        pass

    def get_cores(self) -> int:
        pass
