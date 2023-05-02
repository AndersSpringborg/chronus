import logging
import time

from chronus.domain.configuration import Configurations
from chronus.domain.interfaces.application_runner_interface import ApplicationRunnerInterface
from chronus.domain.interfaces.cpu_info_service_interface import CpuInfoServiceInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.interfaces.system_service_interface import SystemServiceInterface
from chronus.domain.Run import Run


class BenchmarkService:
    cpu: str
    gflops: float
    cpu_info_service: CpuInfoServiceInterface
    application_runner: ApplicationRunnerInterface
    system_service: SystemServiceInterface
    run_repository: RepositoryInterface
    frequency = 20

    def __init__(
        self,
        cpu_info_service: CpuInfoServiceInterface,
        application_runner: ApplicationRunnerInterface,
        system_service: SystemServiceInterface,
        benchmark_repository: RepositoryInterface,
    ):
        self.energy_used = 0.0
        self.cpu_info_service = cpu_info_service
        self.application_runner = application_runner
        self.system_service = system_service
        self.run_repository = benchmark_repository
        self.gflops = 0.0
        self.logger = logging.getLogger(__name__)

    def run(self):
        cpu = self.cpu_info_service.get_cpu_info()

        configurations = Configurations(cpu)
        for configuration in configurations:
            self.logger.info(
                f"Starting benchmark for {cpu.name} with {configuration.cores} cores and {configuration.frequency / 1.0e6} GHz"
            )
            run = Run(
                cpu=cpu.name,
                cores=configuration.cores,
                frequency=configuration.frequency,
                threads_per_core=configuration.threads_per_core,
            )
            self.application_runner.prepare()
            self.application_runner.run(configuration.cores, configuration.frequency)
            while self.application_runner.is_running():
                sample = self.system_service.sample()
                run.add_sample(sample)
                time.sleep(1)

            run.add_sample(self.system_service.sample())
            run.finish()
            run.gflops = self.application_runner.gflops
            run.flop = self.application_runner.result
            self.application_runner.cleanup()
            self.run_repository.save(run)

            self.logger.info(
                f"Benchmark for {cpu} with {configuration.cores} cores and {configuration.frequency} MHz complete, GFLOPS: {run.gflops}"
            )
