from chronus.application.init_model_service import ModelService
from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.Run import Run
from tests.application.fixtures import FakeBencmarkRepository, FakeCpuInfoService


class FakeOptimizer(OptimizerInterface):
    def __init__(self, return_id: int):
        self.id = return_id

    def make_model(self, runs: list[Run]) -> None:
        return


def test_model_service_returns_id_on_save(tmp_path):
    # arrange
    repository = FakeBencmarkRepository()
    optimizer = FakeOptimizer(return_id=1)
    sys_info = FakeCpuInfoService()

    model_service = ModelService(repository, optimizer, sys_info)

    # act
    model_id = model_service.run(str(tmp_path / "optimizer"))

    # assert
    assert model_id == 1
