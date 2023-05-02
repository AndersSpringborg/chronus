from chronus.domain.cpu_info import CpuInfo


class CpuInfoServiceInterface:
    def get_cpu_info(self) -> CpuInfo:
        pass
