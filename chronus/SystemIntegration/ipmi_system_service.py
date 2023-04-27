import datetime

from chronus.domain.interfaces.system_service_interface import SystemServiceInterface
from chronus.domain.system_sample import SystemSample


class IpmiSystemService(SystemServiceInterface):
    def sample(self) -> SystemSample:
        return SystemSample(datetime.datetime.now(), current_power_draw=10.0)
