from dataclasses import dataclass
from typing import List

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


