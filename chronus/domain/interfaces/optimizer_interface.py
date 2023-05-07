from chronus.domain.configuration import Configuration
from chronus.domain.cpu_info import SystemInfo
from chronus.domain.Run import Run


class OptimizerInterface:
    @staticmethod
    def name() -> str:
        raise NotImplementedError()

    def name(self) -> str:
        return self.__class__.name()

    def make_model(self, runs: list[Run]) -> None:
        raise NotImplementedError()

    def save(self, path_without_file_extension: str) -> None:
        raise NotImplementedError()

    def load(self, path: str, path_to_save_locally) -> None:
        raise NotImplementedError()

    def run(self, path_local_model: str) -> Configuration:
        raise NotImplementedError()


class OptimizerRepositoryInterface:
    def save(self, optimizer: OptimizerInterface) -> str:
        raise NotImplementedError()

    def load(self, optimizer_id: str) -> OptimizerInterface:
        raise NotImplementedError()
