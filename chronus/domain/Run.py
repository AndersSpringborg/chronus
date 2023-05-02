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
    threads_per_core: int = 1
    frequency: float = 0.0
    gflops: float = 0.0
    flop: float = 0.0
    start_time: datetime.datetime = None
    end_time: datetime.datetime = None
    benchmark_id: int = None

    def __post_init__(self):
        self._samples = []
        self.start_time = datetime.datetime.now()
        self._gflops_per_watt = None
        self._energy_used_joules = None

    @property
    def gflops_per_watt(self) -> float:
        if self._gflops_per_watt is None:
            self._gflops_per_watt = self.gflops / self._average_power_draw()
        return self._gflops_per_watt

    def _average_power_draw(self) -> float:
        if len(self._samples) == 0:
            return 1.0
        return sum([sample.current_power_draw for sample in self._samples]) / len(self._samples)

    def finish(self, end_time: datetime.datetime = None):
        self.end_time = end_time or datetime.datetime.now()

    @property
    def energy_used_joules(self) -> float:
        if self._energy_used_joules is None:
            self._energy_used_joules = self._calculate_energy_used_joules()
        return self._energy_used_joules

    def _calculate_energy_used_joules(self) -> float:
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
