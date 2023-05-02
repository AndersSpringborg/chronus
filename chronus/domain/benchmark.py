import datetime
from dataclasses import dataclass

from chronus.domain.cpu_info import CpuInfo


@dataclass
class Benchmark:
    system_info: CpuInfo
    application: str
    id: int = None
    created_at: datetime = datetime.datetime.now()
