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
    _joules_used: float = 0.0

    def __post_init__(self):
        self._samples = []

    @property
    def gflops_per_watt(self) -> float:
        return self.gflops / self.watts

    @property
    def energy_used(self) -> float:
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
