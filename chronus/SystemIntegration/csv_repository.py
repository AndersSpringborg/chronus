from chronus.domain.Run import Run
from chronus.domain.interfaces.benchmark_run_repository_interface import BenchmarkRunRepositoryInterface


class CsvRunRepository(BenchmarkRunRepositoryInterface):

    def __init__(self, path: str):
        self.path = path
        if self._file_exists():
            self._backup_file()
        self._create_file()

    def _file_exists(self) -> bool:
        import os
        return os.path.exists(self.path)

    def _create_file(self) -> None:
        with open(self.path, "x") as f:
            f.write("cpu,cores,frequency,gflops,energy_used\n")

    def save(self, run: Run) -> None:
        with open(self.path, "a") as f:
            f.write(f"{run.cpu},{run.cores},{run.frequency},{run.gflops},{run.energy_used}\n")

    def _backup_file(self):
        import os
        os.rename(self.path, f"{self.path}.bak")
