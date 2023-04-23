from typing import List

from dataclasses import dataclass


@dataclass
class Configuration:
    cores: int
    frequency: float


def make_core_interval(cores_number: int):
    cores = []
    counter = 1
    while counter <= cores_number:
        cores.append(counter)
        counter *= 2

    return cores


def make_configurations(cores_number: int, frequencies: List[float]):
    cores = make_core_interval(cores_number)

    configurations = []
    for core in cores:
        for frequency in frequencies:
            configurations.append(Configuration(core, frequency))
    return configurations


class Configurations:
    def __init__(self, cores: int, frequencies: List[float]):
        self.__configurations = make_configurations(cores, frequencies)

    def __iter__(self):
        return iter(self.__configurations)

    def __len__(self):
        return len(self.__configurations)

    def __getitem__(self, index):
        return self.__configurations[index]
