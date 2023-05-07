from chronus.domain.LocalSettings import LocalSettings


class SettingsInterface:
    def save_settings(self, settings: LocalSettings):
        raise NotImplementedError()
