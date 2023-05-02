from chronus.domain.Run import Run
from chronus.domain.benchmark import Benchmark


class RepositoryInterface:
    def save_run(self, run: Run) -> None:
        pass

    def get_all(self) -> list[Run]:
        pass

    def save_benchmark(self, benchmark: Benchmark) -> None:
        pass
