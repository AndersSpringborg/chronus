from chronus.application.model_service import ModelService
from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.Run import Run
from tests.application.fixtures import FakeBencmarkRepository


class FakeOptimizer(OptimizerInterface):
    def __init__(self, return_id: int):
        self.id = return_id

    def make_model(self, runs: list[Run]) -> None:
        return


def test_model_service_returns_id_on_save():
    # arrange
    repository = FakeBencmarkRepository()
    optimizer = FakeOptimizer(return_id=1)

    model_service = ModelService(repository, optimizer)

    # act
    id = model_service.init_model()

    # assert
    assert id == 1
