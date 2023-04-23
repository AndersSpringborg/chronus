import time

from chronus.domain.configuration import Configurations
from chronus.domain.interfaces.application_runner_interface import ApplicationRunnerInterface
from chronus.domain.interfaces.benchmark_run_repository_interface import (
    BenchmarkRunRepositoryInterface,
)
from chronus.domain.interfaces.cpu_info_service_interface import CpuInfoServiceInterface
from chronus.domain.interfaces.system_service_interface import SystemServiceInterface
from chronus.domain.Run import Run


class BenchmarkService:
    cpu: str
    gflops: float
    cpu_info_service: CpuInfoServiceInterface
    application_runner: ApplicationRunnerInterface
    system_service: SystemServiceInterface
    run_repository: BenchmarkRunRepositoryInterface
    frequency = 20

    def __init__(
        self,
        cpu_info_service: CpuInfoServiceInterface,
        application_runner: ApplicationRunnerInterface,
        system_service: SystemServiceInterface,
        benchmark_repository: BenchmarkRunRepositoryInterface,
    ):
        self.energy_used = 0.0
        self.cpu_info_service = cpu_info_service
        self.application_runner = application_runner
        self.system_service = system_service
        self.run_repository = benchmark_repository
        self.gflops = 0.0

    def run(self):
        cpu = self.cpu_info_service.get_cpu_info().cpu
        cores = self.cpu_info_service.get_cores()
        frequencies = self.cpu_info_service.get_frequencies()

        configurations = Configurations(cores, frequencies)
        for configuration in configurations:
            run = Run(cpu=cpu, cores=configuration.cores, frequency=configuration.frequency)
            self.application_runner.run(configuration.cores, configuration.frequency)
            while self.application_runner.is_running():
                sample = self.system_service.sample()
                run.add_sample(sample)
                time.sleep(1)

            run.add_sample(self.system_service.sample())
            run.gflops = self.application_runner.gflops
            self.run_repository.save(run)
