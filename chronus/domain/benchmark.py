import datetime
from dataclasses import dataclass

from chronus.domain.cpu_info import SystemInfo
from chronus.domain.Run import Run


@dataclass
class Benchmark:
    system_info: SystemInfo
    application: str
    id: int = None
    created_at: datetime = datetime.datetime.now()
    runs: list[Run] = None

    def __post_init__(self):
        self.runs = []

    def add_run(self, run: Run):
        run.benchmark_id = self.id
        self.runs.append(run)
