from chronus.domain.Run import Run


class BenchmarkRunRepositoryInterface:
    def save(self, run: Run) -> None:
        pass
