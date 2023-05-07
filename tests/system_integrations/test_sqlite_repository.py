import freezegun
import pytest

from chronus.domain.benchmark import Benchmark
from chronus.domain.cpu_info import SystemInfo
from chronus.domain.Run import Run
from chronus.domain.system_sample import SystemSample
from chronus.SystemIntegration.repositories.sqlite_repository import SqliteRepository
from tests.fixtures import datetime_from_string


@pytest.fixture
def sqlite_db(tmp_path):
    path = tmp_path / "test.db"
    path.touch()
    return path


def test_if_table_exists_and_empty(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    # Act

    # Assert
    assert sqlite_db.exists()
    assert len(repo.get_all_runs()) == 0


@freezegun.freeze_time("2020-01-01 00:00:1")
def test_save_run(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9, benchmark_id=1)
    run.add_sample(
        SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:1"), current_power_draw=10.0)
    )
    run.add_sample(
        SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:2"), current_power_draw=10.0)
    )
    run.finish(datetime_from_string("2020-01-01 00:00:02"))

    # Act
    repo.save_run(run)

    # Assert
    run_saved = repo.get_all_runs()[0]
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
    initial_run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9, benchmark_id=1)
    initial_run.start_time = start_time
    initial_run.end_time = end_time
    initial_run.add_sample(
        SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:01"), current_power_draw=10.0)
    )
    initial_run.add_sample(
        SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:02"), current_power_draw=10.0)
    )

    # Act
    repo.save_run(initial_run)
    run = repo.get_all_runs()[0]

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
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9, benchmark_id=1)
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
    repo.save_run(run)
    saved_run = repo.get_all_runs()[0]
    saved_samples = saved_run.samples

    # Assert
    assert len(saved_samples) == 2


def test_sample_have_correct_data(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9, benchmark_id=1)
    sample1 = SystemSample(
        timestamp=datetime_from_string("2020-01-01 00:00:1"), current_power_draw=10.0
    )
    sample2 = SystemSample(
        timestamp=datetime_from_string("2020-01-01 00:00:2"), current_power_draw=12.0
    )
    run.add_sample(sample1)
    run.add_sample(sample2)
    run.finish(datetime_from_string("2020-01-01 00:00:02"))
    repo.save_run(run)

    # Act
    saved_run = repo.get_all_runs()[0]
    saved_samples = saved_run.samples

    # Assert
    assert saved_samples[0].current_power_draw == 10.0
    assert saved_samples[1].current_power_draw == 12.0
    assert saved_samples[0].timestamp == datetime_from_string("2020-01-01 00:00:1")
    assert saved_samples[1].timestamp == datetime_from_string("2020-01-01 00:00:2")


def test_sample_have_cpu_temps(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9, benchmark_id=1)
    sample1 = SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:1"), cpu_temp=50.0)
    sample2 = SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:2"), cpu_temp=60.0)
    run.add_sample(sample1)
    run.add_sample(sample2)
    run.finish(datetime_from_string("2020-01-01 00:00:02"))
    repo.save_run(run)

    # Act
    saved_run = repo.get_all_runs()[0]
    saved_samples = saved_run.samples

    # Assert
    assert saved_samples[0].cpu_temp == 50.0
    assert saved_samples[1].cpu_temp == 60.0


def test_sample_have_cpu_power(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9, benchmark_id=1)
    sample1 = SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:1"), cpu_power=50.0)
    sample2 = SystemSample(timestamp=datetime_from_string("2020-01-01 00:00:2"), cpu_power=60.0)
    run.add_sample(sample1)
    run.add_sample(sample2)
    run.finish(datetime_from_string("2020-01-01 00:00:02"))
    repo.save_run(run)

    # Act
    saved_run = repo.get_all_runs()[0]
    saved_samples = saved_run.samples

    # Assert
    assert saved_samples[0].cpu_power == 50.0
    assert saved_samples[1].cpu_power == 60.0


def test_benchmark_have_runs(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    benchmark = Benchmark(application="test", system_info=SystemInfo(cores=2))
    run1 = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)
    run2 = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)
    benchmark_id = repo.save_benchmark(benchmark)
    benchmark.id = benchmark_id

    # Act
    benchmark.add_run(run1)
    benchmark.add_run(run2)
    repo.save_run(run1)
    repo.save_run(run2)

    # Assert
    saved_benchmark = repo.get_all_benchmarks()[0]
    assert len(saved_benchmark.runs) == 2


def test_saving_benchmark_saves_runs(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    benchmark = Benchmark(application="test", system_info=SystemInfo(cores=2), id=1)
    run1 = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)
    run2 = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)

    # Act
    benchmark.add_run(run1)
    benchmark.add_run(run2)
    repo.save_benchmark(benchmark)

    # Assert
    saved_benchmark = repo.get_all_benchmarks()[0]
    assert len(saved_benchmark.runs) == 2


def test_cannot_save_runs_without_benchmark_id(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    run = Run(cpu="test", cores=2, frequency=1.5, gflops=30.0, flop=30.0e9)

    # Act
    with pytest.raises(ValueError):
        repo.save_run(run)


def test_getting_runs_from_a_specific_system(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    sys1 = SystemInfo(cpu_name="sys1")
    benchmark1 = Benchmark(id=1, system_info=sys1, application="")
    benchmark1.add_run(Run(cpu="run1"))

    sys2 = SystemInfo(cpu_name="sys2")
    benchmark2 = Benchmark(
        id=2,
        system_info=sys2,
        application="",
    )
    benchmark2.add_run(Run(cpu="run2"))

    repo.save_benchmark(benchmark1)
    repo.save_benchmark(benchmark2)

    # Act
    runs = repo.get_all_runs_from_system(sys2)

    # Assert
    assert len(runs) == 1
    assert runs[0].cpu == "run2"


def test_get_all_system_info(sqlite_db):
    # Arrange
    repo = SqliteRepository(sqlite_db)
    sys1 = SystemInfo(cpu_name="sys1")
    benchmark1 = Benchmark(id=1, system_info=sys1, application="")
    sys2 = SystemInfo(cpu_name="sys2")
    benchmark2 = Benchmark(
        id=2,
        system_info=sys2,
        application="",
    )
    repo.save_benchmark(benchmark1)
    repo.save_benchmark(benchmark2)

    # Act
    systems = repo.get_all_system_info()

    # Assert
    assert len(systems) == 2
    assert systems[0].cpu_name == "sys1"
    assert systems[1].cpu_name == "sys2"
