from chronus.domain.benchmark import Benchmark
from chronus.domain.model import Model
from chronus.domain.Run import Run


class RepositoryInterface:
    def save_run(self, run: Run) -> None:
        pass

    def get_all_runs(self) -> list[Run]:
        pass

    def save_benchmark(self, benchmark: Benchmark) -> int:
        pass

    def get_all_benchmarks(self) -> list[Benchmark]:
        pass

    def save_model(self, model: Model) -> int:
        pass
