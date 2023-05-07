from chronus.domain.benchmark import Benchmark
from chronus.domain.cpu_info import SystemInfo
from chronus.domain.model import Model
from chronus.domain.Run import Run


class RepositoryInterface:
    def save_run(self, run: Run) -> None:
        raise NotImplementedError()

    def get_all_runs(self) -> list[Run]:
        raise NotImplementedError()

    def get_all_runs_from_system(self, system_info) -> list[Run]:
        raise NotImplementedError()

    def save_benchmark(self, benchmark: Benchmark) -> int:
        raise NotImplementedError()

    def get_all_benchmarks(self) -> list[Benchmark]:
        raise NotImplementedError()

    def get_all_system_info(self) -> list[SystemInfo]:
        raise NotImplementedError()

    def save_model(self, model: Model) -> int:
        raise NotImplementedError()

    def get_all_models(self) -> list[Model]:
        raise NotImplementedError()

    def get_model(self, model_id: int) -> Model:
        raise NotImplementedError()
