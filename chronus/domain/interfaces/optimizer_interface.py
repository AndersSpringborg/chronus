from chronus.domain.Run import Run


class OptimizerInterface:
    def make_model(self, runs: list[Run]) -> None:
        pass
