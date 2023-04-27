import time
from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from chronus.domain.benchmark_service import BenchmarkService
from chronus.domain.interfaces.application_runner_interface import ApplicationRunnerInterface
from chronus.domain.interfaces.benchmark_run_repository_interface import (
    BenchmarkRunRepositoryInterface,
)
from chronus.domain.interfaces.cpu_info_service_interface import CpuInfo, CpuInfoServiceInterface
from chronus.domain.interfaces.system_service_interface import SystemServiceInterface
from chronus.domain.system_sample import SystemSample


class FakeCpuInfoService(CpuInfoServiceInterface):
    def __init__(self, cores=4, frequencies=None):
        if frequencies is None:
            frequencies = [1.0, 2.0, 3.0]
        self.cores = cores
        self.frequencies = frequencies

    def get_cores(self):
        return self.cores

    def get_frequencies(self):
        return self.frequencies

    def get_cpu_info(self) -> CpuInfo:
        return CpuInfo(cpu="Fake CPU")


class FakeSystemService(SystemServiceInterface):
    def __init__(self, power_draw=1.0):
        self.power_draw = power_draw

    def sample(self) -> SystemSample:
        return SystemSample(timestamp=datetime.now(), current_power_draw=self.power_draw)


class FakeApplication(ApplicationRunnerInterface):
    def __init__(self, seconds: int):
        self.seconds = seconds
        self.__counter = 0
        self.gflops = 10.0
        self.cleanup_called = 0
        self.prepare_called = 0

    def run(self, cores: int, frequency: float):
        pass

    def prepare(self):
        self.prepare_called += 1

    def cleanup(self):
        self.cleanup_called += 1

    def is_running(self) -> bool:
        is_running = self.__counter < self.seconds
        self.__counter += 1

        return is_running


class FakeBencmarkRepository(BenchmarkRunRepositoryInterface):
    called = 0

    def save(self, benchmark):
        self.called += 1


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
    benchmark_repository: BenchmarkRunRepositoryInterface = None,
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
    benchmark = benchmark_fixture()
    benchmark.run()

    assert benchmark.gflops is not None


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
    assert benchmark_run_repository.called == 2


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
    assert application_runner.prepare_called == 2
