import freezegun
import pytest

from chronus.domain.Run import Run
from chronus.domain.system_sample import SystemSample
from chronus.SystemIntegration.repositories.sqlite_repository import SqliteRepository
from tests.fixtures import datetime_from_string


@pytest.fixture
def sqlite_db(tmp_path):
    return tmp_path / "test.db"


def test_if_table_exists_and_empty(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    # Act

    # Assert
    assert sqlite_db.exists()
    assert len(repo.get_all()) == 0


@freezegun.freeze_time("2020-01-01 00:00:1")
def test_save_run(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)
    run.add_sample(
        SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:1"), current_power_draw=10.0)
    )
    run.add_sample(
        SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:2"), current_power_draw=10.0)
    )
    run.finish(datetime_from_string("2020-01-01 00:00:02"))

    # Act
    repo.save(run)

    # Assert
    run_saved = repo.get_all()[0]
    assert run_saved.cpu == "test"
    assert run_saved.cores == 2
    assert run_saved.frequency == 1.5
    assert run_saved.gflops == 30.0
    assert run_saved.flop == 30.0e9
    assert run_saved.energy_used_joules == 10.0
    assert run_saved.gflops_per_watt == 3.0
    assert datetime_from_string("2020-01-01 00:00:01") == run_saved.start_time


def test_saving_a_run_can_be_loaded_with_the_same_values(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    start_time = datetime_from_string("2020-01-01 00:00:01")
    end_time = datetime_from_string("2020-01-01 00:00:02")
    initial_run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)
    initial_run.start_time = start_time
    initial_run.end_time = end_time
    initial_run.add_sample(
        SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:01"), current_power_draw=10.0)
    )
    initial_run.add_sample(
        SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:02"), current_power_draw=10.0)
    )

    # Act
    repo.save(initial_run)
    run = repo.get_all()[0]

    # Assert
    assert run.cpu == "test"
    assert run.cores == 2
    assert run.frequency == 1.5
    assert run.threads_per_core == 1
    assert run.gflops == 30.0
    assert run.flop == 30.0e9
    assert run


def test_save_run_with_system_samples(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)
    sample1 = SystemSample(
        timestamp=datetime_from_string("2020-01-01 00:00:1"), current_power_draw=10.0
    )
    sample2 = SystemSample(
        timestamp=datetime_from_string("2020-01-01 00:00:2"), current_power_draw=12.0
    )
    run.add_sample(sample1)
    run.add_sample(sample2)
    run.finish(datetime_from_string("2020-01-01 00:00:02"))

    # Act
    repo.save(run)
    saved_run = repo.get_all()[0]
    saved_samples = saved_run._samples

    # Assert
    assert len(saved_samples) == 2


def test_sample_have_correct_data(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)
    sample1 = SystemSample(
        timestamp=datetime_from_string("2020-01-01 00:00:1"), current_power_draw=10.0
    )
    sample2 = SystemSample(
        timestamp=datetime_from_string("2020-01-01 00:00:2"), current_power_draw=12.0
    )
    run.add_sample(sample1)
    run.add_sample(sample2)
    run.finish(datetime_from_string("2020-01-01 00:00:02"))
    repo.save(run)

    # Act
    saved_run = repo.get_all()[0]
    saved_samples = saved_run._samples

    # Assert
    assert saved_samples[0].current_power_draw == 10.0
    assert saved_samples[1].current_power_draw == 12.0
    assert saved_samples[0].timestamp == datetime_from_string("2020-01-01 00:00:1")
    assert saved_samples[1].timestamp == datetime_from_string("2020-01-01 00:00:2")


def test_sample_have_cpu_temps(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)
    sample1 = SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:1"), cpu_temp=50.0)
    sample2 = SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:2"), cpu_temp=60.0)
    run.add_sample(sample1)
    run.add_sample(sample2)
    run.finish(datetime_from_string("2020-01-01 00:00:02"))
    repo.save(run)

    # Act
    saved_run = repo.get_all()[0]
    saved_samples = saved_run._samples

    # Assert
    assert saved_samples[0].cpu_temp == 50.0
    assert saved_samples[1].cpu_temp == 60.0


def test_sample_have_cpu_power(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)
    sample1 = SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:1"), cpu_power=50.0)
    sample2 = SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:2"), cpu_power=60.0)
    run.add_sample(sample1)
    run.add_sample(sample2)
    run.finish(datetime_from_string("2020-01-01 00:00:02"))
    repo.save(run)

    # Act
    saved_run = repo.get_all()[0]
    saved_samples = saved_run._samples

    # Assert
    assert saved_samples[0].cpu_power == 50.0
    assert saved_samples[1].cpu_power == 60.0
