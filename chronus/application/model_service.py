# load model - look if there is a model saved in the model repository
# init model - make a model if there is no model saved in the model repository
#  - get data
# - if there is no data, make data
# - if there is data, load data
#  - train model
# - pure ModelService
from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface


# - test/train?


class ModelService:
    def __init__(self, repository: RepositoryInterface, optimizer: OptimizerInterface):
        self.repository = repository
        self.optimizer = optimizer

    def load_model(self):
        pass

    def init_model(self):
        runs = self.repository.get_all_runs()
        self.optimizer.make_model(runs)

    def list_models(self):
        pass
