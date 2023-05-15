# load model - look if there is a model saved in the model repository
# init model - make a model if there is no model saved in the model repository
#  - get data
# - if there is no data, make data
# - if there is data, load data
#  - train model
# - pure ModelService
import logging
import os
from datetime import datetime

from chronus.domain.interfaces.cpu_info_service_interface import CpuInfoServiceInterface
from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.model import Model

# - test/train?


class InitModelService:
    repository: RepositoryInterface
    optimizer: OptimizerInterface

    def __init__(
        self,
        repository: RepositoryInterface,
        optimizer: OptimizerInterface,
        system_id: int,
    ):
        self.repository = repository
        self.optimizer = optimizer
        self.system_id = system_id
        self.__logger = logging.getLogger(__name__)
        self.__optimizer_dir = "optimizer"

    def run(self) -> int:
        self.__logger.info("Initializing model getting data")
        system = self.__get_system()
        runs = self.repository.get_all_runs_from_system(system)

        self.__logger.info("Initializing model training model")
        self.__ensure_optimizer_dir()
        self.optimizer.make_model(runs)
        full_path_to_model = os.path.abspath(self.__optimizer_dir + "/" + str(hash(self.optimizer)))
        self.optimizer.save(full_path_to_model)

        model = Model(
            name="model_name",
            system_info=system,
            type=self.optimizer.name(),
            path_to_model=full_path_to_model,
            created_at=datetime.now(),
        )

        model_id = self.repository.save_model(model)
        self.__logger.info(f"Initializing model saving model with id {model_id}")

        return model_id

    def list_models(self):
        pass

    def __get_system(self):
        systems = self.repository.get_all_system_info()
        for i, system in enumerate(systems):
            if i == self.system_id:
                self.__logger.info(f"Using system {system}")
                return system

        raise ValueError(f"System with id {self.system_id} not found")

    def __ensure_optimizer_dir(self):
        if not os.path.isdir(self.__optimizer_dir):
            os.mkdir(self.__optimizer_dir)
