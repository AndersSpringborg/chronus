from typing import List

from dataclasses import dataclass

from chronus.domain.cpu_info import CpuInfo


@dataclass
class Configuration:
    cores: int = 0
    frequency: float = 0.0
    threads_per_core: int = 0


def make_core_interval(cores_number: int):
    cores = []
    counter = 1
    while counter <= cores_number:
        cores.append(counter)
        counter *= 2

    return cores


def make_configurations(cpu_info: CpuInfo) -> List[Configuration]:
    cores = make_core_interval(cpu_info.cores)

    configurations = []
    for core in cores:
        for thread in range(1, cpu_info.threads_per_core + 1):
            for frequency in cpu_info.frequencies:
                configurations.append(Configuration(core, frequency, thread))
    return configurations


class Configurations:
    def __init__(self, cpu_info: CpuInfo):
        self.__configurations = make_configurations(cpu_info)

    def __iter__(self):
        return iter(self.__configurations)

    def __len__(self):
        return len(self.__configurations)

    def __getitem__(self, index):
        return self.__configurations[index]
