import logging

from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.Run import Run

CSV_HEADERS = "cpu,cores,thread_per_core,frequency,gflops,gflop,energy_used,gflops_per_watt,start_time,end_time\n"


class CsvRunRepository(RepositoryInterface):
    date_time_format = "%Y-%m-%d %H:%M:%S"

    def get_all(self) -> list[Run]:
        # make datetime parse 2023-04-27 16:00:36.435748
        with open(self.path) as f:
            rows = f.readlines()
            runs = []
            for row in rows[1:]:
                run = Run()
                (
                    cpu,
                    cores,
                    thread_per_core,
                    frequency,
                    gflops,
                    gflop,
                    energy_used,
                    gflops_per_watt,
                    start_time,
                    end_time,
                ) = row.split(",")

                run.cpu = cpu
                run.cores = int(cores)
                run.threads_per_core = int(thread_per_core)
                run.frequency = float(frequency)
                run.gflops = float(gflops)
                run.flop = float(gflop) * 1.0e9
                run._energy_used_joules = float(energy_used)
                run._gflops_per_watt = float(gflops_per_watt)
                runs.append(run)
        return runs

    def save(self, run: Run) -> None:
        with open(self.path, "a") as f:
            gflop = run.flop / 1.0e9
            f.write(
                f"{run.cpu},{run.cores},{run.threads_per_core},{run.frequency},{run.gflops},{gflop},{run.energy_used_joules},{run.gflops_per_watt},{run.start_time},{run.end_time}\n"
            )
        self.logger.info(f"Run data has been saved to {self.path}.")

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

    def _backup_file(self):
        import os

        os.rename(self.path, f"{self.path}.bak")
        self.logger.info(f"{self.path} has been backed up to {self.path}.bak.")
