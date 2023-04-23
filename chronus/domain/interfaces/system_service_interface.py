from chronus.domain.system_sample import SystemSample


class SystemServiceInterface:
    def sample(self) -> SystemSample:
        pass
