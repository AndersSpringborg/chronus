from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Run:
    fan_speed_rpm: int = 0
    cpu_temp_c: float = 0.0
    cpu_cores: int = 0
    cpu_clock: float = 0.0
    cpu_load: float = 0.0
    gflops: float = 0.0
    watts: float = 0.0

    @property
    def gflops_per_watt(self) -> float:
        return self.gflops / self.watts
