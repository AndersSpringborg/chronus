import datetime
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from chronus.domain.system_sample import SystemSample


@dataclass_json
@dataclass(init=True, repr=True, eq=True, order=True)
class Run:
    _samples: list[SystemSample] = None
    cpu: str = ""
    cores: int = 0
    frequency: float = 0.0
    gflops: float = 0.0
    start_time: datetime.datetime = None
    end_time: datetime.datetime = None

    def __post_init__(self):
        self._samples = []
        self.start_time = datetime.datetime.now()

    @property
    def gflops_per_watt(self) -> float:
        return self.gflops / self._average_power_draw()

    def _average_power_draw(self) -> float:
        return sum([sample.current_power_draw for sample in self._samples]) / len(self._samples)

    def finish(self, end_time: datetime.datetime = None):
        self.end_time = end_time or datetime.datetime.now()

    @property
    def energy_used_joules(self) -> float:
        energy = 0.0
        previous_timestamp = self._samples[0].timestamp if len(self._samples) > 0 else None
        previous_power_draw = (
            self._samples[0].current_power_draw if len(self._samples) > 0 else None
        )
        for sample in self._samples:
            time_delta = (sample.timestamp - previous_timestamp).total_seconds()
            average_power = (sample.current_power_draw + previous_power_draw) / 2
            energy += average_power * time_delta
            previous_timestamp = sample.timestamp
        return energy

    def add_sample(self, sample: SystemSample):
        self._samples.append(sample)
