from chronus.domain.interfaces.benchmark_run_repository_interface import BenchmarkRunRepositoryInterface


class CsvRunRepository(BenchmarkRunRepositoryInterface):

    def __init__(self, path: str):
        self.path = path
    def save(self, benchmark) -> None:
        print(benchmark)
