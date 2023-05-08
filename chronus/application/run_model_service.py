import logging

from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.interfaces.settings_interface import LocalStorageInterface


class RunModelService:
    def __init__(self, local_storage: LocalStorageInterface, optimizer: OptimizerInterface):
        self.__logger = logging.getLogger(__name__)
        self.local_storage = local_storage
        self.optimizer = optimizer

    def run(self):
        model = self.local_storage.get_settings().loaded_model
        conf = self.optimizer.run(self.local_storage.get_full_path("/model"))

        return conf
