import datetime
from dataclasses import dataclass

from chronus.domain.cpu_info import SystemInfo


@dataclass
class Model:
    name: str
    system_info: SystemInfo
    path_to_model: str
    type: str  # Nordjyske bank
    created_at: datetime
    id: int = None
