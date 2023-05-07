import dataclasses
import json
from dataclasses import dataclass

from chronus.domain.configuration import Configuration
from chronus.domain.cpu_info import SystemInfo
from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.Run import Run


class BruteForceOptimizer(OptimizerInterface):
    @staticmethod
    def name() -> str:
        return "brute-force"

    __best_run: Configuration = None

    def make_model(self, runs: list[Run]) -> None:
        self.__best_run = Configuration()
        best_efficiency = 0.0

        for run in runs:
            efficiency = energy_efficiency(run)
            if efficiency > best_efficiency:
                best_efficiency = efficiency
                self.__best_run.cores = run.cores
                self.__best_run.threads_per_core = run.threads_per_core
                self.__best_run.frequency = run.frequency

    def save(self, path_without_file_extension: str) -> None:
        # save to a file in the path
        with open(path_without_file_extension + ".json", "w") as file:
            file.write(json.dumps(dataclasses.asdict(self.__best_run)))

    def load(self, optimizer_id: str) -> None:
        # load from a file in the path
        with open(optimizer_id + ".json") as file:
            run = json.loads(file.read())
            self.__best_run = Configuration(**run)

    def run(self, sys_info: SystemInfo) -> Configuration:
        return self.__best_run


def energy_efficiency(run: Run) -> float:
    return run.gflops_per_watt
