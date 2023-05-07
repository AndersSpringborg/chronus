from enum import Enum

from chronus.domain.LocalSettings import LocalSettings


class Permission(Enum):
    READ = 1
    WRITE = 2


class LocalStorageInterface:
    def __init__(self, mode: Permission):
        raise NotImplementedError()

    def save_settings(self, settings: LocalSettings):
        raise NotImplementedError()

    def get_settings(self) -> LocalSettings:
        raise NotImplementedError()

    def get_full_path(self, relative_path: str):
        raise NotImplementedError()
