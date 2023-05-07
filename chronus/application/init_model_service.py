# load model - look if there is a model saved in the model repository
# init model - make a model if there is no model saved in the model repository
#  - get data
# - if there is no data, make data
# - if there is data, load data
#  - train model
# - pure ModelService
import logging
from pprint import pprint

from chronus.domain.interfaces.cpu_info_service_interface import CpuInfoServiceInterface
from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.model import Model

# - test/train?


class ModelService:
    repository: RepositoryInterface
    optimizer: OptimizerInterface

    def __init__(
        self,
        repository: RepositoryInterface,
        optimizer: OptimizerInterface,
        system_info_provider: CpuInfoServiceInterface,
    ):
        self.repository = repository
        self.optimizer = optimizer
        self.system_info_provider = system_info_provider
        self.__logger = logging.getLogger(__name__)

    def load_model(self):
        pass

    def run(self, path) -> int:
        self.__logger.info("Initializing model getting data")
        system = self.system_info_provider.get_cpu_info()
        runs = self.repository.get_all_runs_from_system(system)

        self.__logger.info("Initializing model training model")
        self.optimizer.make_model(runs)
        self.optimizer.save(path)

        model = Model(
            name="model_name",
            system_info=system,
            type=self.optimizer.name,
            path_to_model="path/to/model",
            created_at="2021-01-01",
        )

        model_id = self.repository.save_model(model)
        self.__logger.info(f"Initializing model saving model with id {model_id}")

        return model_id

    def list_models(self):
        pass
