# 1 load model from optimizer
# 2 save model to local storage
# 3 set /etc/chronus/model to the model
import logging
import os

from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.interfaces.settings_interface import LocalStorageInterface
from chronus.domain.LocalSettings import LocalSettings


class LoadModelService:
    def __init__(
        self,
        repository: RepositoryInterface,
        optimizer: OptimizerInterface,
        local_storage: LocalStorageInterface,
        model_id: int,
    ):
        self.repository = repository
        self.optimizer = optimizer
        self.model_id = model_id
        self.local_storage = local_storage
        self.__logger = logging.getLogger(__name__)

        self.__model_file_name = "model"

    def run(self):
        model = self.repository.get_model(self.model_id)
        full_model_path = self.local_storage.get_full_path(self.__model_file_name)
        self.optimizer.load(model.path_to_model, full_model_path)
        self.__logger.info(f"Loaded model {model.name} from {model.path_to_model} to local machine")

        settings_to_load = LocalSettings(loaded_model=model)

        self.local_storage.save_settings(settings_to_load)
