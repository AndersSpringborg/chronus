import datetime
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from chronus.domain.system_sample import SystemSample


@dataclass_json
@dataclass(init=True, repr=True, eq=True, order=True)
class Run:
    samples: list[SystemSample] = None
    cpu: str = ""
    cores: int = 0
    threads_per_core: int = 1
    frequency: int = 0.0
    gflops: float = 0.0
    flop: float = 0.0
    start_time: datetime.datetime = None
    end_time: datetime.datetime = None
    benchmark_id: int = None
    __gflops_per_watt: float = None
    __energy_used_joules: float = None

    def __post_init__(self):
        self.samples = []
        self.start_time = datetime.datetime.now()

    @property
    def gflops_per_watt(self) -> float:
        if self.__gflops_per_watt is None:
            self.__gflops_per_watt = self.gflops / self._average_power_draw()
        return self.__gflops_per_watt

    def _average_power_draw(self) -> float:
        if len(self.samples) == 0:
            return 1.0
        return sum([sample.current_power_draw for sample in self.samples]) / len(self.samples)

    def finish(self, end_time: datetime.datetime = None):
        self.end_time = end_time or datetime.datetime.now()

    @property
    def energy_used_joules(self) -> float:
        if self.__energy_used_joules is None:
            self.__energy_used_joules = self._calculate_energy_used_joules()
        return self.__energy_used_joules

    def _calculate_energy_used_joules(self) -> float:
        energy = 0.0
        previous_timestamp = self.samples[0].timestamp if len(self.samples) > 0 else None
        previous_power_draw = self.samples[0].current_power_draw if len(self.samples) > 0 else None
        for sample in self.samples:
            time_delta = (sample.timestamp - previous_timestamp).total_seconds()
            average_power = (sample.current_power_draw + previous_power_draw) / 2
            energy += average_power * time_delta
            previous_timestamp = sample.timestamp
        return energy

    def add_sample(self, sample: SystemSample):
        self.samples.append(sample)
