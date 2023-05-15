from typing import List

from dataclasses import dataclass

import dataclasses_json

from chronus.domain.cpu_info import SystemInfo


@dataclass
class Configuration:
    cores: int = 0
    frequency: int = 0
    threads_per_core: int = 0


def make_core_interval(cores_number: int):
    cores = []
    counter = 1
    while counter <= cores_number:
        cores.append(counter)
        counter *= 2

    return cores


def make_configurations(cpu_info: SystemInfo) -> list[Configuration]:
    cores = make_core_interval(cpu_info.cores)

    configurations = []
    for core in cores:
        for thread in range(1, cpu_info.threads_per_core + 1):
            for frequency in cpu_info.frequencies:
                configurations.append(Configuration(core, frequency, thread))
    return configurations


@dataclasses_json.dataclass_json
class Configurations:
    def __init__(self, cpu_info: SystemInfo):
        self.__configurations = make_configurations(cpu_info)

    def __iter__(self):
        return iter(self.__configurations)

    def __len__(self):
        return len(self.__configurations)

    def __getitem__(self, index):
        return self.__configurations[index]
