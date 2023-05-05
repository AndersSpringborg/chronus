# load model - look if there is a model saved in the model repository
# init model - make a model if there is no model saved in the model repository
#  - get data
# - if there is no data, make data
# - if there is data, load data
#  - train model
# - pure ModelService
import logging
from pprint import pprint

from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.model import Model

# - test/train?


class ModelService:
    def __init__(self, repository: RepositoryInterface, optimizer: OptimizerInterface):
        self.repository = repository
        self.optimizer = optimizer
        self._logger = logging.getLogger(__name__)

    def load_model(self):
        pass

    def run(self):
        self._logger.info("Initializing model getting data")
        runs = self.repository.get_all_runs()

        self._logger.info("Initializing model training model")

        optimizer = self.optimizer.make_model(runs)

        optimizer.save_local_on_machine("path/to/model")  # blob
        model = Model(
            name="model_name",
            optimizer=optimizer,
        )

        model_id = self.repository.save_model(model)

        return model_id

    def list_models(self):
        pass
