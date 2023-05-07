# 1 load model from optimizer
# 2 save model to local storage
# 3 set /etc/chronus/model to the model
import logging
import os

from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.LocalSettings import LocalSettings


class LoadModelService:
    def __init__(
        self,
        repository: RepositoryInterface,
        optimizer: OptimizerInterface,
        model_id: int,
    ):
        self.repository = repository
        self.optimizer = optimizer
        self.model_id = model_id
        self.__logger = logging.getLogger(__name__)

        self.__local_model_path = "/etc/chronus/model"
        self.__local_settings_path = "/etc/chronus/settings.json"

    def run(self):
        model = self.repository.get_model(self.model_id)
        self.optimizer.load(model.path_to_model, self.__local_model_path)
        self.__logger.info(f"Loaded model {model.name} from {model.path_to_model} to local machine")

        # mkdirs for /etc/chronus/model if it doesn't exist
        os.makedirs(os.path.dirname(self.__local_model_path), exist_ok=True)
        settings_to_load = LocalSettings(loaded_model=model)

        # save model id to /etc/chronus/model
        with open(self.__local_model_path, "w") as f:
            f.write(settings_to_load.to_json())
