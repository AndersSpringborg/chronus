import datetime
from dataclasses import dataclass

from chronus.domain.cpu_info import CpuInfo


@dataclass
class Model:
    name: str
    system_info: CpuInfo
    path_to_model: str
    type: str  # Nordjyske bank
    created_at: datetime
    id: int = None
