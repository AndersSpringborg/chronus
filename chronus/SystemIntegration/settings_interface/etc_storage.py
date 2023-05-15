import logging
import os

from chronus.domain.interfaces.settings_interface import LocalStorageInterface, Permission
from chronus.domain.LocalSettings import LocalSettings


class EtcLocalStorage(LocalStorageInterface):
    def __init__(self, mode: Permission):
        self.__logger = logging.getLogger(__name__)
        self.__local_root = "/etc/chronus"
        self.__local_settings_path = "/etc/chronus/settings.json"

        if mode == Permission.WRITE:
            self.__ensure_etc_chronus_is_created()

    def __ensure_etc_chronus_is_created(self):
        self.__logger.info("This is installing the model system wide (requires root)")
        try:
            os.makedirs(self.__local_root, exist_ok=True)
            self.__logger.info(f"Created {self.__local_root}")
        except PermissionError:
            self.__logger.error("Permission denied to create /etc/chronus. Please run as root.")
            raise

    def save_settings(self, settings: LocalSettings):
        with open(self.__local_settings_path, "w") as f:
            f.write(settings.to_json())

    def get_settings(self) -> LocalSettings:
        with open(self.__local_settings_path) as f:
            return LocalSettings.from_json(f.read())

    def get_full_path(self, relative_path: str):
        return self.__local_root + "/" + relative_path
