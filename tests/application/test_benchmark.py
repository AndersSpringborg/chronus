import logging
import time
from datetime import timedelta

import freezegun
import pytest
from freezegun import freeze_time

from chronus.application.benchmark_service import BenchmarkService
from chronus.domain.benchmark import Benchmark
from chronus.domain.cpu_info import SystemInfo
from chronus.domain.interfaces.application_runner_interface import ApplicationRunnerInterface
from chronus.domain.interfaces.cpu_info_service_interface import CpuInfoServiceInterface
from chronus.domain.interfaces.repository_interface import RepositoryInterface
from chronus.domain.interfaces.system_service_interface import SystemServiceInterface
from tests.application.fixtures import (
    FakeApplication,
    FakeBencmarkRepository,
    FakeCpuInfoService,
    FakeSystemService,
)
from tests.fixtures import datetime_from_string


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
    benchmark = Benchmark(id=100, application="test", system_info=SystemInfo())
    repository = FakeBencmarkRepository(benchmark=benchmark)
    benchmark_service = benchmark_fixture(benchmark_repository=repository)

    # Act
    benchmark_service.run()

    # Assert
    run = repository.runs[0]
    assert run.benchmark_id == benchmark.id


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
    cpu_info_service = FakeCpuInfoService(cores=2, frequencies=[1.0])
    benchmark = benchmark_fixture(
        cpu_info_service=cpu_info_service,
        application=application_runner,
    )

    # Act
    benchmark.run()

    # Assert
    assert application_runner.cleanup_called == 2


def test_calls_cleanup_when_application_raises_job_error(skip_sleep, caplog):
    # Arrange
    application_runner = FakeApplication(4, raise_job_error=True)
    cpu_info_service = FakeCpuInfoService(cores=1, frequencies=[1.0])
    benchmark = benchmark_fixture(
        cpu_info_service=cpu_info_service,
        application=application_runner,
    )

    # Act
    benchmark.run()

    # Assert
    assert (
        "ERROR    chronus.application.benchmark_service:benchmark_service.py:64 Job failed with config 1 cores, 1e-06 GHz and 1 threads per core\n"
        in caplog.text
    )


def test_logger_outputs_config_on_job_failure(skip_sleep):
    # Arrange
    application_runner = FakeApplication(4, raise_job_error=True)
    cpu_info_service = FakeCpuInfoService(cores=1, frequencies=[1.0])
    benchmark = benchmark_fixture(
        cpu_info_service=cpu_info_service,
        application=application_runner,
    )

    # Act
    benchmark.run()

    # Assert
    assert application_runner.cleanup_called == 1


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
