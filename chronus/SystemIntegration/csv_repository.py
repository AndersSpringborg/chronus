import logging

from chronus.domain.interfaces.benchmark_run_repository_interface import (
    BenchmarkRunRepositoryInterface,
)
from chronus.domain.Run import Run

CSV_HEADERS = "cpu,cores,frequency,gflops,energy_used,gflops_per_watt,start_time,end_time\n"


class CsvRunRepository(BenchmarkRunRepositoryInterface):
    def __init__(self, path: str):
        self.logger = logging.getLogger(__name__)
        self.path = path
        if self._file_exists():
            self._backup_file()
        self._create_file()

    def _file_exists(self) -> bool:
        import os

        if os.path.exists(self.path):
            self.logger.info(f"File {self.path} already exists.")
            return True
        return False

    def _create_file(self) -> None:
        with open(self.path, "x") as f:
            f.write(CSV_HEADERS)
        self.logger.info(f"File {self.path} has been created.")

    def save(self, run: Run) -> None:
        with open(self.path, "a") as f:
            f.write(
                f"{run.cpu},{run.cores},{run.frequency},{run.gflops},{run.energy_used_joules},{run.gflops_per_watt},{run.start_time},{run.end_time}\n"
            )
        self.logger.info(f"Run data has been saved to {self.path}.")

    def _backup_file(self):
        import os

        os.rename(self.path, f"{self.path}.bak")
        self.logger.info(f"{self.path} has been backed up to {self.path}.bak.")
