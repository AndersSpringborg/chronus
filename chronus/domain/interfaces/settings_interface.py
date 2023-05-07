from chronus.domain.LocalSettings import LocalSettings


class LocalStorageInterface:
    def save_settings(self, settings: LocalSettings):
        raise NotImplementedError()

    def get_full_path(self, relative_path: str):
        raise NotImplementedError()
