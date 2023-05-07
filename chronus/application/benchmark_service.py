import logging
import time

from chronus.domain.benchmark import Benchmark
from chronus.domain.configuration import Configurations
from chronus.domain.interfaces.application_runner_interface import ApplicationRunnerInterface
from chronus.domain.interfaces.cpu_info_service_interface import CpuInfoServiceInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.interfaces.system_service_interface import SystemServiceInterface
from chronus.domain.Run import Run


class JobFailedException(Exception):
    pass


class BenchmarkService:
    cpu: str
    gflops: float
    cpu_info_service: CpuInfoServiceInterface
    application_runner: ApplicationRunnerInterface
    system_service: SystemServiceInterface
    repository: RepositoryInterface
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
        self.repository = benchmark_repository
        self.gflops = 0.0
        self.logger = logging.getLogger(__name__)

    def run(self):
        cpu = self.cpu_info_service.get_cpu_info()

        benchmark = Benchmark(system_info=cpu, application="HPCG")
        benchmark_id = self.repository.save_benchmark(benchmark)

        configurations = Configurations(cpu)
        for configuration in configurations:
            self.logger.info(
                f"Starting benchmark for {cpu.cpu_name} with {configuration.cores} cores, {configuration.frequency / 1.0e6} GHz and {configuration.threads_per_core} threads per core"
            )
            run = Run(
                cpu=cpu.cpu_name,
                cores=configuration.cores,
                frequency=configuration.frequency,
                threads_per_core=configuration.threads_per_core,
                benchmark_id=benchmark_id,
            )
            self.application_runner.prepare()
            self.application_runner.run(configuration.cores, configuration.frequency)
            try:
                self._wait_for_application_to_finish_and_save_run(configuration, cpu, run)
            except JobFailedException:
                self.logger.error(
                    f"Job failed with config {configuration.cores} cores, {configuration.frequency / 1.0e6} GHz and {configuration.threads_per_core} threads per core"
                )
            finally:
                self.application_runner.cleanup()

    def _wait_for_application_to_finish_and_save_run(self, configuration, cpu, run):
        while self.application_runner.is_running():
            sample = self.system_service.sample()
            run.add_sample(sample)
            time.sleep(1)
        run.add_sample(self.system_service.sample())
        run.finish()
        run.gflops = self.application_runner.gflops
        run.flop = self.application_runner.result
        self.repository.save_run(run)
        self.logger.info(
            f"Benchmark for {cpu} with {configuration.cores} cores and {configuration.frequency} MHz complete, GFLOPS: {run.gflops}"
        )

    def _save_benchmark(self, benchmark: Benchmark):
        self.repository.save_benchmark(benchmark)
