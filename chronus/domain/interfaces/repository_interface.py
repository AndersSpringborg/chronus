from chronus.domain.Run import Run
from chronus.domain.benchmark import Benchmark


class RepositoryInterface:
    def save_run(self, run: Run) -> None:
        pass

    def get_all_runs(self) -> list[Run]:
        pass

    def save_benchmark(self, benchmark: Benchmark) -> Benchmark:
        pass

    def get_all_benchmarks(self) -> list[Benchmark]:
        pass
