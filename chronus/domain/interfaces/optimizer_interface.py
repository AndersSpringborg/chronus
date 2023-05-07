from chronus.domain.configuration import Configuration
from chronus.domain.cpu_info import SystemInfo
from chronus.domain.Run import Run


class OptimizerInterface:
    @staticmethod
    def name() -> str:
        pass

    def name(self) -> str:
        return self.__class__.name()

    def make_model(self, runs: list[Run]) -> None:
        pass

    def save(self, path_without_file_extension: str) -> None:
        pass

    def load(self, path: str) -> None:
        pass

    def run(self, sys_info: SystemInfo) -> Configuration:
        pass


class OptimizerRepositoryInterface:
    def save(self, optimizer: OptimizerInterface) -> str:
        pass

    def load(self, optimizer_id: str) -> OptimizerInterface:
        pass
