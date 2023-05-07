from chronus.domain.cpu_info import SystemInfo


class CpuInfoServiceInterface:
    def get_cpu_info(self) -> SystemInfo:
        pass
