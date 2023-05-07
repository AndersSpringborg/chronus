import logging
import os

from chronus.domain.interfaces.settings_interface import LocalStorageInterface
from chronus.domain.LocalSettings import LocalSettings


class EtcLocalStorage(LocalStorageInterface):
    def save_settings(self, settings: LocalSettings):
        with open(self.__local_settings_path, "w") as f:
            f.write(settings.to_json())

    def get_full_path(self, relative_path: str):
        return self.__local_root + relative_path

    def __init__(self):
        self.__logger = logging.getLogger(__name__)

        self.__local_root = "/etc/chronus"
        self.__local_settings_path = "/etc/chronus/settings.json"

    def __ensure_etc_chronus_is_created(self):
        self.__logger.info("This is installing the model system wide (requires root)")
        try:
            os.makedirs(os.path.dirname(self.__local_root), exist_ok=True)
        except PermissionError:
            self.__logger.error("Permission denied to create /etc/chronus. Please run as root.")
            raise
