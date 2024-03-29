from chronus.application.init_model_service import InitModelService
from chronus.domain.configuration import Configuration
from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.Run import Run
from tests.application.fixtures import FakeBencmarkRepository, FakeCpuInfoService


class FakeOptimizer(OptimizerInterface):
    def save(self, path_without_file_extension: str) -> None:
        pass

    def load(self, path: str, path_to_save_locally) -> None:
        pass

    def run(self, path_local_model: str) -> Configuration:
        pass

    @staticmethod
    def name() -> str:
        return "fake-optimizer"

    def __init__(self, return_id: int):
        self.id = return_id

    def make_model(self, runs: list[Run]) -> None:
        return


def test_init_model_saves_model_to_repo(tmp_path):
    # arrange
    repository = FakeBencmarkRepository()
    optimizer = FakeOptimizer(return_id=1)

    # act
    model_service = InitModelService(repository, optimizer, 0)
    model_service.run()

    # assert
    assert len(repository.get_all_models()) == 1
