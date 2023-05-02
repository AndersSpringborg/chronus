import time
from datetime import datetime, timedelta

import freezegun
import pytest
from freezegun import freeze_time

from chronus.application.benchmark_service import BenchmarkService
from chronus.domain.benchmark import Benchmark
from chronus.domain.interfaces.application_runner_interface import ApplicationRunnerInterface
from chronus.domain.interfaces.cpu_info_service_interface import CpuInfoServiceInterface
from chronus.domain.cpu_info import CpuInfo
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.interfaces.system_service_interface import SystemServiceInterface
from chronus.domain.Run import Run
from chronus.domain.system_sample import SystemSample
from tests.fixtures import datetime_from_string


class FakeCpuInfoService(CpuInfoServiceInterface):
    def __init__(self, cores=4, frequencies=None):
        if frequencies is None:
            frequencies = [1.0, 2.0, 3.0]
        self.cores = cores
        self.frequencies = frequencies

    def get_cpu_info(self) -> CpuInfo:
        return CpuInfo(
            name="Fake CPU", cores=self.cores, frequencies=self.frequencies, threads_per_core=1
        )


class FakeSystemService(SystemServiceInterface):
    def __init__(self, power_draw=1.0):
        self.power_draw = power_draw

    def sample(self) -> SystemSample:
        return SystemSample(timestamp=datetime.now(), current_power_draw=self.power_draw)


class FakeApplication(ApplicationRunnerInterface):
    def run(self, cores: int, frequency: float, thread_per_core=1):
        pass

    def __init__(self, seconds: int = None, result: float = None, gflops: float = None):
        self.seconds = seconds or 0
        self.__counter = 0
        self.gflops = gflops or 10.0
        self.result = result or 100.0
        self.cleanup_called = 0
        self.prepare_called = 0

    def prepare(self):
        self.prepare_called += 1

    def cleanup(self):
        self.cleanup_called += 1

    def is_running(self) -> bool:
        is_running = self.__counter < self.seconds
        self.__counter += 1

        return is_running


class FakeBencmarkRepository(RepositoryInterface):
    called_save_run = 0
    runs: list[Run]

    called_save_benchmark = 0
    benchmarks: list[Benchmark]

    def __init__(self, benchmark: Benchmark = None):
        self.runs = []
        self.benchmarks = []
        self._benchmark = benchmark

    def save_run(self, run: Run) -> None:
        self.called_save_run += 1
        self.runs.append(run)

    def save_benchmark(self, benchmark: Benchmark) -> Benchmark:
        self.called_save_benchmark += 1
        self.benchmarks.append(benchmark)
        if self._benchmark is not None:
            return self._benchmark
        return benchmark


@pytest.fixture
def sleepless(monkeypatch):
    def sleep(seconds):
        pass

    monkeypatch.setattr(time, "sleep", sleep)


@pytest.fixture
def skip_sleep(mocker):
    mocked_sleep = mocker.patch("time.sleep")

    def get_mocked_sleep():
        return mocked_sleep

    return get_mocked_sleep


def benchmark_fixture(
    cpu_info_service: CpuInfoServiceInterface = None,
    application: ApplicationRunnerInterface = None,
    system_service: SystemServiceInterface = None,
    benchmark_repository: RepositoryInterface = None,
):
    if cpu_info_service is None:
        cpu_info_service = FakeCpuInfoService(cores=1, frequencies=[1.5])
    if application is None:
        application = FakeApplication(seconds=0)
    if system_service is None:
        system_service = FakeSystemService()
    if benchmark_repository is None:
        benchmark_repository = FakeBencmarkRepository()
    return BenchmarkService(
        cpu_info_service=cpu_info_service,
        application_runner=application,
        system_service=system_service,
        benchmark_repository=benchmark_repository,
    )


def test_initialize_benchmark():
    benchmark = benchmark_fixture()
    assert benchmark is not None


def test_benchmark_have_speed_after_run():
    gflops = 100.0
    repository = FakeBencmarkRepository()
    runner = FakeApplication(gflops=gflops)
    benchmark = benchmark_fixture(
        benchmark_repository=repository,
        application=runner,
    )
    benchmark.run()

    run = repository.runs[0]
    assert run.flop == gflops


def test_run_have_benchmark_id():
    # Arrange
    benchmark = Benchmark(id=100, application="test", system_info=CpuInfo())
    repository = FakeBencmarkRepository(benchmark=benchmark)
    benchmark_service = benchmark_fixture(
        benchmark_repository=repository
    )

    # Act
    benchmark_service.run()

    # Assert
    run = repository.runs[0]
    assert run.benchmark == benchmark


def test_benchmark_have_result_after_run():
    operations_done = 100.0
    repository = FakeBencmarkRepository()
    runner = FakeApplication(result=operations_done)
    benchmark = benchmark_fixture(
        benchmark_repository=repository,
        application=runner,
    )
    benchmark.run()

    run = repository.runs[0]
    assert run.flop == operations_done


def test_benchmark_saved_after_each_configuration(skip_sleep):
    # Arrange
    mock_sleep = skip_sleep()
    cores = 2
    frequencies = [1.0]
    application_runner = FakeApplication(4)
    benchmark_run_repository = FakeBencmarkRepository()
    cpu_info_service = FakeCpuInfoService(cores=cores, frequencies=frequencies)
    benchmark = benchmark_fixture(
        cpu_info_service=cpu_info_service,
        benchmark_repository=benchmark_run_repository,
        application=application_runner,
    )

    # Act
    with freeze_time() as frozen_time:
        mock_sleep.side_effect = lambda seconds: frozen_time.tick(timedelta(seconds=seconds))
        benchmark.run()

    # Assert
    assert benchmark_run_repository.called_save_run == 2


def test_calls_cleanup_after_each_run(skip_sleep):
    # Arrange
    application_runner = FakeApplication(4)
    benchmark_run_repository = FakeBencmarkRepository()
    cpu_info_service = FakeCpuInfoService(cores=2, frequencies=[1.0])
    system_service = FakeSystemService()
    benchmark = benchmark_fixture(
        cpu_info_service=cpu_info_service,
        benchmark_repository=benchmark_run_repository,
        application=application_runner,
        system_service=system_service,
    )

    # Act
    benchmark.run()

    # Assert
    assert application_runner.cleanup_called == 2


def test_calls_prepare_before_each_run(skip_sleep):
    # Arrange
    application_runner = FakeApplication()
    cpu_info_service = FakeCpuInfoService(cores=2, frequencies=[1.0])
    benchmark = benchmark_fixture(
        cpu_info_service=cpu_info_service,
        application=application_runner,
    )

    # Act
    benchmark.run()

    # Assert
    assert application_runner.prepare_called == 2


@freezegun.freeze_time("2021-01-01 00:00:00")
def test_benchmark_set_end_time_after_run_is_completed(skip_sleep):
    # Arrange
    repository = FakeBencmarkRepository()
    benchmark = benchmark_fixture(
        benchmark_repository=repository,
    )

    # Act
    benchmark.run()

    # Assert
    run = repository.runs[0]
    assert run.end_time == datetime_from_string("2021-01-01 00:00:00")


def test_saves_benchmark_benchmark_model_on_every_run(skip_sleep):
    # Arrange
    repository = FakeBencmarkRepository()
    benchmark = benchmark_fixture(
        benchmark_repository=repository,
    )

    # Act
    benchmark.run()

    # Assert
    assert repository.called_save_benchmark == 1
    assert len(repository.benchmarks) == 1
