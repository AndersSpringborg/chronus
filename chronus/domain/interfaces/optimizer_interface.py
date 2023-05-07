from chronus.domain.configuration import Configuration
from chronus.domain.cpu_info import CpuInfo
from chronus.domain.Run import Run


class OptimizerInterface:
    @staticmethod
    def name() -> str:
        pass

    def make_model(self, runs: list[Run]) -> None:
        pass

    def save(self, path: str) -> None:
        pass

    def load(self, path: str) -> None:
        pass

    def run(self, sys_info: CpuInfo) -> Configuration:
        pass
